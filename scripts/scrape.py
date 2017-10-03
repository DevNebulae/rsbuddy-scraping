#!/usr/bin/python3
'''
The run module which scrapes and stores RSBuddy data in
JSON files.
'''
import logging
import json
from random import shuffle
import argparse
import cfscrape
from fsutils.writing import write_file
import numpy as np
from threaded.retriever import Retriever
from scrapeutils.cache import cached

parser = argparse.ArgumentParser()

parser.add_argument('--threads', help='Increase the amount of threads which will retrieve the data. Be warned that this will also increase the amount of bandwidth the script needs.')
parser.add_argument('--start', help='Define the start of the financial transactions.')
parser.add_argument('--retries', help='Define the maximum amount of times the script will try to download the data.')

def main():
    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
    file_handler = logging.FileHandler('scraper.log')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.debug('Started downloading items.')

    scraper = cfscrape.create_scraper()
    items = cached(scraper, '.data/items.json', 'https://rsbuddy.com/exchange/names.json')

    # Write caching file to .data folder
    write_file('.data/items.json', json.dumps(items))

    logger.debug('Finished downloading items.')

    # Divide the items into buckets for the retrievers to
    # process
    thread_amount = int(args.threads) if args.threads else 2
    timestamp = int(args.start) if args.start else 1420070400000
    max_retries = int(args.retries) if args.retries else 5

    threads = []
    item_ids = list(items.keys())
    shuffle(item_ids)
    item_id_buckets = np.array_split(item_ids, thread_amount)

    logger.debug('Started downloading item history.')

    # Create all retrievers and run them as a seperate
    # thread
    for item_id_bucket in item_id_buckets:
        thread = Retriever(item_id_bucket, timestamp, scraper, max_retries, logger)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logger.debug('Scraper finished.')

if __name__ == "__main__":
    main()
