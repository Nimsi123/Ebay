def is_good_response(resp):
	"""
	Returns True if the response seems to be HTML, False otherwise.
	"""
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200 
			and content_type is not None 
			and content_type.find('html') > -1)

def log_error(e):
	"""
	It is always a good idea to log errors. 
	This function just prints them, but you can
	make it do anything.
	"""
	print(e)

def simple_get(url, testing = False):
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				if testing:
					return resp.text
				else:
					return resp.content
			else:
				return None
	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None

"""def simple_get(driver, url):
	driver.get(url)
	return driver.page_source"""