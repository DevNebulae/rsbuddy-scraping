#!/usr/bin/python3
import os
from fsutils.json import read_json
from pprint import pprint
from reducer import Reducer
import numpy as np
from pymongo import MongoClient

def main():
    if not os.path.exists('.data/items.json'):
        raise Exception('The items.json file in the .data folder does not exist. Please run the scraping script before executing this script.')

    collection_name = 'rsbuddy'
    client = MongoClient('localhost', 27017)
    database = client[collection_name]

    items = list(read_json('.data/items.json').items())
    indexes = np.array_split(np.arange(len(items)), len(items) // 50)
    threads = []
    thread_count = 2

    for index in range(len(indexes)):
        indexes_ = indexes[index]

        thread = Reducer(database, collection_name, indexes_, items)
        thread.start()
        threads.append(thread)

        if (index % thread_count == 0 and index != 0):
            for thread in threads:
                thread.join()

            threads = []

if __name__ == "__main__":
    main()
