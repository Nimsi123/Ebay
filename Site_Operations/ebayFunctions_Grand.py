from Ebay.ItemOrganization.Item import Item
from Ebay.Site_Operations.cleanEntries import clean_title, clean_price, clean_shipping, clean_date
from Ebay.Site_Operations.traverseHtml import findElement, findAllLetters, findKey, findLink
from bs4 import BeautifulSoup
import bs4


def make_eBay_link(listing_type, search_str):
	"""
	Returns a starting link for a search query.

	>>> make_eBay_link("Auction", "Jimi Hendrix Poster")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Jimi Hendrix Poster&LH_Sold=1&LH_Complete=1&rt=nc&LH_Auction=1&_ipg=200'
	>>> make_eBay_link("Buy It Now", "Cream Disraeli Gears")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Cream Disraeli Gears&LH_Sold=1&LH_Complete=1&rt=nc&LH_BIN=1&_ipg=200'

	"""
	assert listing_type in ["All Listings", "Auction", "Buy It Now"], "not a valid listing type. Must be one of 'All Listings', 'Auction', or 'Buy It Now'"

	link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + search_str + "&LH_Sold=1&LH_Complete=1"

	if listing_type == "All Listings":
		pass
	elif listing_type == "Auction":
		link += "&rt=nc&LH_Auction=1"
	elif listing_type == "Buy It Now":
		link += "&rt=nc&LH_BIN=1"

	return link + "&_ipg=200"


def extract(get_raw_func, html, element_type, class_name, clean_func):
	"""
	html -> a block of code representing a single listing

	Search the html block for the attribute of an item defined by 'element_type' and 'class_name.'
	Return the result of calling 'clean_func' on the item's attribute.
	"""

	raw = get_raw_func(html, element_type, "class", class_name)
	
	if raw == "nothing found":
		return None

	while type(raw) == bs4.Tag:
		#go deeper in a nest
		raw = raw.contents[0]

	return clean_func(str(raw)) #usable format for my algorithm

def extract_nested(get_raw_func, html, outer_element_type, outer_class_name, inner_element_type, inner_class_name, clean_func):
	"""
	Some attributes are nested within two blocks.
	Returns the attribute accessed by diving into one block, and then going deeper.
	"""

	outer_block = findElement(html, outer_element_type, "class", outer_class_name)

	if outer_block == "nothing found":
		return None
	
	outer_block = outer_block.contents[0]
	cleaned_inner = extract(get_raw_func, outer_block, inner_element_type, inner_class_name, clean_func)

	return cleaned_inner


def searchListings(html, element_type, class_code, item_collection, printer_bool_page_stats = False):
	"""
	html -> html code for an entire webpage

	Adds new items to item_collection.
	"""

	#ebay tries to mess with the sale date and my code
	#right before the code starts, I will find the special class_name that can be used to find the sale date!
	key = findKey(html, element_type, ["S", "o", "l", "d"])

	count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code = 0, 0, 0, 0

	for listing in html.find_all(element_type):
		if listing.get("class") == None:
			count_skipped_early += 1
			continue
		else:
			class_name = listing.get("class")[0]

		if class_name == class_code:
			#extract data from a single listing

			title = extract(findElement, listing, "h3", "s-item__title", clean_title)
			price = extract(findElement, listing, "span", "s-item__price", clean_price)
			shipping = extract(findElement, listing, "span", "s-item__shipping", clean_shipping)

			if key == None:
				date = extract(findElement, listing, "div", "s-item__title--tagblock", clean_date)
			else:
				print("*****need to do extra work to get sale date********MANDOLORIAN")
				date = extract_nested(findAllLetters, listing, "div", "s-item__title--tagblock", "span", key, clean_date)

			if all([attr is not None for attr in [title, price, date, shipping]])
				total_cost = round(price+shipping, 2)
				item_collection.addItem( Item(title, total_cost, date) )
				count_added += 1
			else:
				#print(f"BAD LISTING -- title: {title} price: {price} shipping: {shipping} date: {date}")
				count_skipped_bad += 1

		else:
			count_skipped_class_code += 1

	if printer_bool_page_stats:
		printer_page_stats_one(len(html.find_all(element_type)), count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code)

def receive_html(client, link):
	"""
	Returns the html from a webpage as a BeautifulSoup object.
	"""

	raw_html = client.get(url = link).text
	html = BeautifulSoup(raw_html, 'html.parser')

	return html

def printer_product_stats(total_listings, max_iteration):
	print("\nPRODUCT STATS")
	print("{0:30}: {1}".format("total_listings", total_listings))
	print("{0:30}: {1}".format("max_iteration", max_iteration))
	print("\n")

def printer_page_stats_one(num_item_listings, count_added, count_skipped_early, count_skipped_bad, count_skipped_class_code):
	print("\nPAGE STATS")
	print("{0:30}: {1}".format("num item listings", num_item_listings))
	print("{0:30}: {1}".format("count added", count_added))
	print("----")
	print("{0:30}: {1}".format("count_skipped_early", count_skipped_early))
	print("{0:30}: {1}".format("count_skipped_bad", count_skipped_bad))
	print("{0:30}: {1}".format("count_skipped_class_code", count_skipped_class_code))
	print("----")

def printer_page_stats_two(count, item_list_length, link, date_appended):
	print("{0:30}: {1}".format("current item_list length", item_list_length))
	print("{0:30}: {1}".format("iter count", count))
	print("{0:30}: {1}".format("link", link))
	print("{0:30}: {1}".format("EARLIEST DATE", date_appended))
	print("--------")

def is_overlapping(date_stored, date_appended):
	if (date_stored and date_appended) and (date_appended < date_stored):
		print("\n")
		print("**********************Broken the loop*************************")
		print(date_appended)
		print("**************************************************************")
		return True

def aboutALink(client, link, product_collection, date_stored = None, printer_bool_product_stats = True, printer_bool_page_stats = True):
	"""
	Starting from 'link', make requests to client for webpages' html code. 
	Populate 'product_collection' with new items listed on the webpage.
	Continue until we reach the end of the pages with listings.
	"""

	html = receive_html(client, link)

	strip_comma = lambda entry: entry.replace(',', '')
	temp_num = extract(findElement, html, "h1", "srp-controls__count-heading", strip_comma)
	
	print("\naboutALink")
	print("{0:30}: {1}".format("link", link))
	print("{0:30}: {1}".format("extract", temp_num))
	
	total_listings = int(temp_num)

	if total_listings == 0:
		return

	max_iteration = min(50, int(total_listings/200 +1)) #ebay won't show us more that 10,000 items from their page even though there might be more to look at

	if printer_bool_product_stats:
		printer_product_stats(total_listings, max_iteration)

	for count in range(max_iteration):

		html = receive_html(client, link)
		searchListings(html, "li", "s-item", product_collection, printer_bool_page_stats)

		date_appended = product_collection.earliest_date()
		
		if printer_bool_page_stats:
			printer_page_stats_two(count, len(product_collection.item_list), link, date_appended)

		if is_overlapping(date_stored, date_appended):
			break

		link = findLink(link)