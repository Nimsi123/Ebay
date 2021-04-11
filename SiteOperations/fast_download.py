from concurrent.futures.thread import ThreadPoolExecutor
import time
from bs4 import BeautifulSoup

from eBayScraper.SiteOperations.clean_entries import NOT_FOUND
from eBayScraper.SiteOperations.traverse_html import next_link, extract, is_overlapping, search_listings, get_listings_iteration, find_key
from eBayScraper.SiteOperations import printer
from eBayScraper.data_files.directories import HTML_STORE_DIR
from eBayScraper.ItemOrganization.timer import timer

THREAD_LIMIT = 5
REQUEST_WAIT = 0.5
MAX_PAGES = 50
ITEM_PER_PAGE = 200


"""
TODO: 
OPTIMIZATION: find the key once. don't find the key for every listing.
"""

def link_generator(link):
	link += "&_pgn=1"
	while True:
		yield link

		end = old_link.find("&_pgn=") + len("&_pgn=")
		link = old_link[:end] + str(int(old_link[end:]) + 1)

def html_download(client, url, i):
	"""Get the HTML from the eBay page and export it to the file 'scrape_{i}.txt' for the parameter i.

	:param url: The link to the eBay page.
	:type url: str
	:param i: The page number counter.
	:type i: int
	"""

	with open(HTML_STORE_DIR.format(i), "w", encoding = "utf-8") as file:
		file.write(client.get(url).text)

def yield_html(client, link, page_count):
	"""Responsible for yielding html pages. Counters stay within THREAD_LIMIT and MAX_PAGES.
	"""
	count = 0
	yield_link = link_generator(link)

	@timer
	def run_threads():
		nonlocal count

		sub_c = 0
		#run threads and download html
		with ThreadPoolExecutor(max_workers=THREAD_LIMIT) as executor:
			while sub_c < THREAD_LIMIT and count < min(MAX_PAGES, page_count):
				link = next(yield_link)
				print("LINK: ", link)
				executor.submit(html_download, client, link, count)
				time.sleep(REQUEST_WAIT)

				sub_c += 1
				count += 1

		return (count - sub_c, count)

	while count < min(MAX_PAGES, page_count):

		interval = run_threads()

		for i in range(*interval):
			#receive and parse html from text file
			with open(HTML_STORE_DIR.format(i), "r", encoding = "utf-8") as raw_html:
				html = BeautifulSoup(raw_html, 'html.parser')
				yield html

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

	if total_listings is NOT_FOUND and page_count is NOT_FOUND:
		return total_listings

	if print_stats:
		printer.product_stats(total_listings, page_count)

	count = 0
	storage.reset_count_added()
	for html in yield_html(client, link, page_count):
		# if a key is used by eBay, every page has a unique key. 
		# only need to find it once per page.
		key = find_key(html, ["S", "o", "l", "d"])

		date = None
		for title, price, date in search_listings(html, key, print_stats): # search_listings might yield nothing!
			storage.add_item(title, price, date, sale_type)

		oldest_date = date #the oldest date just added is the one last assigned in the for loop above
		count += 1
		if print_stats:
			printer.page_stats_two(count, storage.get_count_added(), oldest_date)

		if is_overlapping(recent_date_stored, oldest_date) and not deep_scrape:
			return total_listings

	return total_listings