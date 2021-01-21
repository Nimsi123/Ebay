from concurrent.futures.thread import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup

from Ebay.SiteOperations import printer
from Ebay.SiteOperations.traverseHtml import next_link, extract, is_overlapping, search_listings, get_listings_iteration

#constants
THREAD_LIMIT = 5
REQUEST_WAIT = 0.5
MAX_PAGES = 50
ITEM_PER_PAGE = 200

def html_download(client, url, i):
	"""Get the HTML from the eBay page and export it to the file 'scrape_{i}.txt' for the parameter i.

	:param url: The link to the eBay page.
	:type url: str
	:param i: The page number counter.
	:type i: int
	"""

	with open(f"../HTML_Store/scrape_{i}.txt", "w", encoding = "utf-8") as file:
		file.write(client.get(url).text)

def fast_download(client, product_collection, link, date_stored, print_stats, deep_scrape):
	"""
	This function is called once for every query.
	Until we reach an overlap point or page_count, iterate through the query's eBay pages and populate product_collection with Item data.
	Use threads to download html concurrently. Iterate sequentially through the html text and convert to Item data.
	"""

	html = BeautifulSoup(client.get(link).text, 'html.parser')
	total_listings, page_count = get_listings_iteration(html)

	if total_listings is None and max_iteration is None:
		return

	if print_stats:
		printer.product_stats(total_listings, page_count)

	count = 0
	while count < min(MAX_PAGES, page_count):

		sub_c = 0
		#run threads and download html
		with ThreadPoolExecutor(max_workers=THREAD_LIMIT) as executor:
			while sub_c < THREAD_LIMIT and count < min(MAX_PAGES, page_count):
				executor.submit(html_download, client, link, count)
				time.sleep(REQUEST_WAIT)

				link = next_link(link)
				sub_c += 1
				count += 1

		#digest html
		for i in range(count - sub_c, count):
			#receive and parse html from text file
			with open(f"../HTML_Store/scrape_{i}.txt", "r", encoding = "utf-8") as raw_html:
				html = BeautifulSoup(raw_html, 'html.parser')

			search_listings(html, "li", "s-item", product_collection, print_stats)

			date_appended = product_collection.earliest_date()
			if print_stats:
				printer.page_stats_two(count, len(product_collection.item_list), link, date_appended)

			if is_overlapping(date_stored, date_appended) and not deep_scrape:
				return