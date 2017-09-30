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
from retriever import retriever
from scraper_utils import cached

def main():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.log(logging.INFO, 'Start downloading items')

    scraper = cfscrape.create_scraper()
    items = cached(scraper, '.data/items.json', 'https://rsbuddy.com/exchange/names.json')

    # Write caching file to .data folder
    write_file('.data/items.json', json.dumps(items))

    # Divide the items into buckets for the retrievers to
    # process
    # TODO: Add command line options for these variables
    threads = 4
    start = 1420070400000
    max_retries = 5

    item_ids = list(items.keys())[:100]
    shuffle(item_ids)
    item_id_buckets = np.array_split(item_ids, threads)

    logger.log(logging.INFO, 'Start downloading item history')

    # Create all retrievers and run them as a seperate
    # thread
    for item_id_bucket in item_id_buckets:
        thread = Thread(target=retriever, args=(item_id_bucket, start, scraper, max_retries, logger))
        thread.start()

if __name__ == "__main__":
    main()
