from bs4 import BeautifulSoup

from Ebay.SiteOperations import printer
from Ebay.ItemOrganization.Item import Item
from Ebay.SiteOperations.clean_entries import clean_title, clean_price, clean_shipping, clean_date
from Ebay.SiteOperations.traverseHtml import find_element, find_letters, find_key, next_link, is_overlapping, extract, search_listings, get_listings_iteration

def receive_html(client, link):
	"""Returns the html from a webpage as a BeautifulSoup object.
	"""

	return BeautifulSoup(client.get(url = link).text, 'html.parser')

def about_a_link(client, link, product_collection, date_stored = None, print_stats = True):
	"""
	Starting from 'link', make requests to client for webpages' html code. 
	Populate 'product_collection' with new items listed on the webpage.
	Continue until we reach the end of the pages with listings.
	"""

	html = receive_html(client, link)

	total_listings, max_iteration = get_listings_iteration(html)

	if total_listings is None and max_iteration is None:
		return

	if print_stats:
		printer.product_stats(total_listings, max_iteration)

	for count in range(max_iteration):

		html = receive_html(client, link)
		search_listings(html, "li", "s-item", product_collection, print_stats)

		date_appended = product_collection.earliest_date()
		
		if print_stats:
			printer.page_stats_two(count, len(product_collection.item_list), link, date_appended)

		if is_overlapping(date_stored, date_appended):
			break

		link = next_link(link)