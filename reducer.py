from functools import reduce
from fsutils.json import read_json
from threading import Thread
import os

class Reducer(Thread):
    def __init__(self, database, collection_name, indexes, items):
        super(Reducer, self).__init__()

        self.database = database
        self.collection_name = collection_name
        self.indexes = indexes
        self.items = items

    def reduce_items(self, accumulator, index):
        key, value = self.items[index]

        if not os.path.exists(f'.data/{key}.json'):
            return accumulator

        filename = f'.data/{key}.json'
        data = read_json(filename)

        accumulator.append({'id': int(key), **value, 'transactions': data})
        return accumulator

    def run(self):
        items = reduce(self.reduce_items, self.indexes, [])
        self.database[self.collection_name].insert_many(items)
