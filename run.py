#!/usr/bin/python3
'''
The run module which scrapes and stores RSBuddy data in
JSON files.
'''
import cfscrape
from fs_utils import write_file
import json
import numpy as np
from retriever import retriever
from scraper_utils import cached
from threading import Thread

def main():
    scraper = cfscrape.create_scraper()
    items = cached(scraper, '.data/items.json', 'https://rsbuddy.com/exchange/names.json')

    # Write caching file to .data folder
    write_file('.data/items.json', json.dumps(items))

    # Divide the items into buckets for the retrievers to
    # process
    threads = 4
    start = 1420070400000
    item_ids = list(items.keys())
    item_id_buckets = np.array_split(item_ids, threads)

    # Create all retrievers and run them as a seperate
    # thread
    for item_id_bucket in item_id_buckets:
        thread = Thread(target=retriever, args=(item_id_bucket, start, scraper))
        thread.start()

if __name__ == "__main__":
    main()
