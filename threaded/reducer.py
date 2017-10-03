from functools import reduce
from fs_utils import read_json
from threading import Thread

class Reducer(Thread):
    def __init__(self, items):
        super(Reducer, self).__init__()

        self.items = items

    def reduce_items(self, accumulator, item):
        key, value = item
        filename = f'.data/{key}.json'
        data = read_json(filename)

        accumulator.append({'id': int(key), **value, 'transactions': data})
        return accumulator

    def run(self):
        items = reduce(self.reduce_items, self.items, [])
        print(items)
