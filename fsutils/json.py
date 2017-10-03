import json

def read_json(path):
    with open(path) as _file:
        return json.load(_file)
