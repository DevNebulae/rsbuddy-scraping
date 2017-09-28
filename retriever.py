'''
Class module which is meant to asynchronously retrieve all
JSON data from the RSBuddy API.
'''

import json
from fs_utils import write_file
from scraper_utils import scrape

def retriever(item_ids, start, scraper):
    '''
    Function meant as an asynchronous getter for the RSBuddy
    API JSON data. It needs a list of item ids which it will
    fetch, the timestamp (in milliseconds) to where it will
    retrieve the data and the scraper instance which it will
    call.
    '''
    for identifier in item_ids:
        url = f'https://api.rsbuddy.com/grandExchange?a=graph&g=30&start={start}&i={identifier}'
        data = scrape(scraper, url)
        write_file(f'.data/{identifier}.json', json.dumps(data))
