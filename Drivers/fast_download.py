from concurrent.futures.thread import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup

from Ebay.SiteOperations.ebayFunctions_Grand import searchListings, extract, find_element, printer_product_stats, printer_page_stats_two, is_overlapping
from Ebay.SiteOperations.traverseHtml import next_link


THREAD_LIMIT = 5
REQUEST_WAIT = 0.5 # 0.5 seconds is optimal
JOIN_WAIT = 3 # wait until we join threads
MAX_PAGES = 51
ITEM_PER_PAGE = 200

def fast_download(client, product_collection, link, date_stored, printer_bool_product_stats = True, printer_bool_page_stats = True, deep_scrape = False):
	"""
	This function is called once for every query.
	Until we reach an overlap point or page_count, iterate through the query's eBay pages and populate product_collection with Item data.
	Use threads to download html concurrently. Iterate sequentially through the html text and convert to Item data.
	"""

	#calculate page_count
	html = BeautifulSoup(client.get(link).text, 'html.parser')
	total_listings = int(extract(find_element, html, "h1", "srp-controls__count-heading", lambda entry: entry.replace(',', '')))
	page_count = int(total_listings/ITEM_PER_PAGE +1)

	if total_listings == 0:
		return

	if printer_bool_product_stats:
		printer_product_stats(total_listings, page_count)

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

			searchListings(html, "li", "s-item", product_collection, printer_bool_page_stats)

			date_appended = product_collection.earliest_date()
			if printer_bool_page_stats:
				printer_page_stats_two(count, len(product_collection.item_list), link, date_appended)

			if is_overlapping(date_stored, date_appended) and not deep_scrape:
				return

def html_download(client, url, i):
	"""Get the HTML from the eBay page and export it to the file 'scrape_{i}.txt' for the parameter i.

	:param url: The link to the eBay page.
	:type url: str
	:param i: The page number counter.
	:type i: int
	"""

	with open(f"../HTML_Store/scrape_{i}.txt", "w", encoding = "utf-8") as file:
		file.write(client.get(url).text)