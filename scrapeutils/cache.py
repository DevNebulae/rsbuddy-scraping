import json
import os
from scrapeutils.scrape import scrape

def cached(scraper, path, url):
    if os.path.isfile(path):
        with open(path, 'r') as _file:
            return json.load(_file)
    else:
        return json.loads(scrape(scraper, url))
