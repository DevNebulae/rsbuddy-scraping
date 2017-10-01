#!/usr/bin/python3
import os
from fs_utils import read_json
from itertools import chain
from pprint import pprint

def main():
    if not os.path.exists('.data/items.json'):
        raise Exception('The items.json file in the .data folder does not exist. Please run the scraping script before executing this script.')

    lookup = read_json('.data/items.json')
    items = {}

    # TODO: Process in batches of a certain size
    for key, values in list(lookup.items())[:100]:
        filename = f'.data/{key}.json'
        items[key] = {**values, 'transactions': read_json(filename)}

    pprint(items)

if __name__ == "__main__":
    main()
