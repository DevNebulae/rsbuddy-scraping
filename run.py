#!/usr/bin/python3
'''
The run module which scrapes and stores RSBuddy data in
JSON files.
'''
import cfscrape
from fs_utils import write_file
import numpy as np
from retriever import Retriever
from scraper_utils import scrape

def main():
    scraper = cfscrape.create_scraper()
    items = scrape(scraper, 'https://rsbuddy.com/exchange/names.json')

    # Write caching file to .data folder
    write_file('.data/items.json', items)

    # Divide the items into buckets for the retrievers to
    # process
    bucket_size = 4
    start = 1420070400000
    item_id_buckets = np.array_split(list(items.keys())[:20], bucket_size)

    # Create all retrievers and run them as a seperate
    # thread
    for item_id_bucket in item_id_buckets:
        retriever = Retriever(item_id_bucket, start, scraper)
        retriever.start()
        # Kill threads when they take more than 15 minutes,
        # adjust accordingly
        retriever.join(timeout=9000)

if __name__ == "__main__":
    main()
