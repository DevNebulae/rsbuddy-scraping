'''
General utility module which contains generalized code to
retrieve data.
'''

def scrape(scraper, url):
	'''
	Utility function which retrieves data from the specified
	url and decodes it in the latin-1 format.
	'''
    return scraper.get('https://rsbuddy.com/exchange/names.json').content.decode('latin1')
