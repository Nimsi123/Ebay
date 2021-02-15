def make_eBay_link(listing_type, search_str):
	"""
	Returns a starting link for a search query.

	>>> make_link("Auction", "Jimi Hendrix Poster")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Jimi Hendrix Poster&LH_Sold=1&LH_Complete=1&rt=nc&LH_Auction=1&_ipg=200'
	>>> make_link("Buy It Now", "Cream Disraeli Gears")
	'https://www.ebay.com/sch/i.html?_from=R40&_nkw=Cream Disraeli Gears&LH_Sold=1&LH_Complete=1&rt=nc&LH_BIN=1&_ipg=200'
	"""
	assert listing_type in ["All Listings", "Auction", "BIN"], "not a valid listing type. Must be one of 'All Listings', 'Auction', or 'Buy It Now'"

	link = "https://www.ebay.com/sch/i.html?_from=R40&_nkw=" + search_str + "&LH_Sold=1&LH_Complete=1"

	if listing_type == "All Listings":
		pass
	elif listing_type == "Auction":
		link += "&rt=nc&LH_Auction=1"
	elif listing_type == "Buy It Now":
		link += "&rt=nc&LH_BIN=1"

	return link + "&_ipg=200"

def csv_dir(name):
	return f"data_files\\CSV\\{name.replace(' ', '_')}.csv"

def png_dir(name):
	return f"data_files\\PNG\\{name.replace(' ', '_')}_combo.png"

HTML_STORE_DIR = "data_files/HTML_Store/scrape_{}.txt"
BAD_LISTING_DIR = "data_files/bad_listings.csv"
CLIENT_REQUESTS_DIR = "data_files/Client.csv"
JS_JSON_DIR = "web/json.js"