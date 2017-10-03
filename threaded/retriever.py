'''
Class module which is meant to asynchronously retrieve all
JSON data from the RSBuddy API.
'''

import json
import time
from threading import Thread
from fs_utils import write_file
from scraper_utils import scrape

class Retriever(Thread):
    def __init__(self, item_ids, timestamp, scraper, max_retries, logger):
        super(Retriever, self).__init__()

        self.item_ids = item_ids
        # It is called "timestamp" instead of "start",
        # because start is a Thread-reserved function
        self.timestamp = timestamp
        self.scraper = scraper
        self.max_retries = max_retries
        self.logger = logger

    def retrieve(self, item_id, retries):
        if retries < 1:
            # When all attempts have failed, log an error
            self.logger.critical(f'Failed to download item id {item_id} after {self.max_retries} attempts. Please check the API to find the error or try again another time.')
            return

        # Time out the downloading for an exponential
        # increasing amount of seconds before trying to
        # download the data again
        time.sleep(2 ** (self.max_retries - retries) - 1)

        url = f'https://api.rsbuddy.com/grandExchange?a=graph&g=30&start={self.timestamp}&i={item_id}'
        response = scrape(self.scraper, url)

        try:
            content = json.loads(response)
            write_file(f'.data/{item_id}.json', json.dumps(content))

            # Log when an item has been succesfully processed
            self.logger.info(f'Successfully retrieved item id {item_id}\'s price history.')
        # A JSONDecodeError is a child of ValueError
        # TODO: Add JSONDecodeError for clarity
        except ValueError:
            self.logger.warn(f'Attempt to retrieve item id {item_id} failed. Retrying.')

            # When the downloading has not succeeded, try
            # again
            self.retrieve(item_id, retries - 1)

    def run(self):
        for item_id in self.item_ids:
            self.retrieve(item_id, self.max_retries)
