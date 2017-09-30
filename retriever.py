'''
Class module which is meant to asynchronously retrieve all
JSON data from the RSBuddy API.
'''

import json
import logging
import time
from fs_utils import write_file
from scraper_utils import scrape

def retrieve(item_id, start, scraper, max_retries, retries, logger):
    url = f'https://api.rsbuddy.com/grandExchange?a=graph&g=30&start={start}&i={item_id}'
    # Retry downloading the item, but with an exponentially
    # increasing time frame
    time.sleep(2 ** (max_retries - retries + 1))

    if retries < 1:
        # When all attempts have failed, log an error
        logger.log(logging.ERROR, f'Failed to download item id {item_id} after {retries} attempts. Please check the API to find the error or try again another time')
        return

    try:
        data = scrape(scraper, url)
        write_file(f'.data/{item_id}.json', json.dumps(data))

        # Log when an item has been succesfully processed
        logging.log(logging.INFO, f'Successfully retrieved item id {item_id}\'s price history')
    except ValueError:
        # When the downloading has not succeeded, try again
        retrieve(item_id, start, scraper, max_retries, retries - 1, logger)

def retriever(item_ids, start, scraper, max_retries, logger):
    '''
    Function meant as an asynchronous getter for the RSBuddy
    API JSON data. It needs a list of item ids which it will
    fetch, a timestamp (in milliseconds) in the past,
    indicating a timespan from now until the timestamp, and
    the scraper instance which it will call.
    '''
    for item_id in item_ids:
        retrieve(item_id, start, scraper, max_retries, max_retries, logger)
