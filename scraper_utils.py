'''
General utility module which contains generalized code to
retrieve data.
'''

import json
import os

def cached(scraper, path, url):
    if os.path.isfile(path):
        with open(path, 'r') as _file:
            return json.load(_file)
    else:
        return scrape(scraper, url)

def scrape(scraper, url):
    '''
    Utility function which retrieves data from the specified
    url and decodes it in the latin-1 format.
    '''
    return json.loads(scraper.get(url).content.decode('latin1'))
