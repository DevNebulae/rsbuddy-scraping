def scrape(scraper, url):
    '''
    Utility function which retrieves data from the specified
    url and decodes it in the latin-1 format.
    '''
    return scraper.get(url).content.decode('latin1')
