from concurrent.futures.thread import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup

from Ebay.SiteOperations.traverse_html import next_link, extract, is_overlapping, search_listings, get_listings_iteration
from Ebay.SiteOperations import printer
from Ebay.data_files.directories import HTML_STORE_DIR

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

	with open(HTML_STORE_DIR.format(i), "w", encoding = "utf-8") as file:
		file.write(client.get(url).text)

def fast_download(client, storage, sale_type, link, print_stats, deep_scrape):
	"""Adds item data to ``storage``. Item data is collected from every listing posted on the html pages, starting at the ``link``.
	Until we reach an overlap point or page_count, iterate through the eBay pages.
	Use threads to download html concurrently. Iterate sequentially through the html text and stores useful data in ``storage``.

	:param client: The class that provides html-downloading functionality
	:type client: class
	:param storage: The data structure that holds the item data.
	:type storage: pandas.DataFrame
	:param sale_type: The type of listing. For example, items sold at 'Auction' or 'Buy it Now'.
	:type sale_type: str
	:param link: The starting URL for scraping. All future links are obtained by calling next_link(link). 
	:type link: str
	:param print_stats: Determines whether we print stats on the scraping process.
	:type print_stats: bool
	:param deep_scrape: Determines whether we end the search at an overlap point or not.
	:type deep_scrape: bool
	"""
	recent_date_stored = storage.get_recent_date(sale_type)

	html = BeautifulSoup(client.get(link).text, 'html.parser')
	total_listings, page_count = get_listings_iteration(html)

	if total_listings is None and page_count is None:
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

				#print("{0:30}: {1}".format("link", link))
				link = next_link(link)
				sub_c += 1
				count += 1

		#digest html
		storage.reset_count_added()
		for i in range(count - sub_c, count):
			#receive and parse html from text file
			with open(HTML_STORE_DIR.format(i), "r", encoding = "utf-8") as raw_html:
				html = BeautifulSoup(raw_html, 'html.parser')

			date = None
			#ran_for_loop = False
			#print("Before for loop!")
			for title, price, date in search_listings(html, print_stats):
				storage.add_item(title, price, date, sale_type)
				ran_for_loop = True

			#if not ran_for_loop:
				#print("Didn't run the for loop!")

			oldest_date = date #the oldest date just added is the one last assigned in the for loop above
			if print_stats:
				printer.page_stats_two(i, storage.get_count_added(), oldest_date)

			if is_overlapping(recent_date_stored, oldest_date) and not deep_scrape:
				return