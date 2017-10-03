#!/usr/bin/python3
import os
from fsutils.json import read_json
from pprint import pprint
from threaded.reducer import Reducer

def main():
    if not os.path.exists('.data/items.json'):
        raise Exception('The items.json file in the .data folder does not exist. Please run the scraping script before executing this script.')

    lookup = read_json('.data/items.json')

    reducer = Reducer(list(lookup.items())[:100])
    reducer.start()
    reducer.join()

if __name__ == "__main__":
    main()
