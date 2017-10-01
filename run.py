#!/usr/bin/python3
'''
The run module which scrapes and stores RSBuddy data in
JSON files.
'''
import logging
import json
from threading import Thread
from random import shuffle
import cfscrape
from fs_utils import touch_dir, write_file
import numpy as np
from retriever import Retriever
from scraper_utils import cached

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.info('Started downloading items.')

    scraper = cfscrape.create_scraper()
    items = cached(scraper, '.data/items.json', 'https://rsbuddy.com/exchange/names.json')

    # Write caching file to .data folder
    write_file('.data/items.json', json.dumps(items))

    logger.debug('Finished downloading items.')

    # Divide the items into buckets for the retrievers to
    # process
    # TODO: Add command line options for these variables
    thread_amount = 4
    timestamp = 1420070400000
    max_retries = 5

    threads = []
    item_ids = list(items.keys())[:100]
    shuffle(item_ids)
    item_id_buckets = np.array_split(item_ids, thread_amount)

    logger.info('Start downloading item history')

    # Create all retrievers and run them as a seperate
    # thread
    for item_id_bucket in item_id_buckets:
        thread = Retriever(item_id_bucket, timestamp, scraper, max_retries, logger)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
