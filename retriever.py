'''
Class module which is meant to asynchronously retrieve all
JSON data from the RSBuddy API.
'''

from threading import Thread
from scraper_utils import scrape

class Retriever(Thread):
	'''
	Class meant as an asynchronous getter for the RSBuddy
	API JSON data. It needs a list of item ids which it will
	fetch, the timestamp (in milliseconds) to where it will
	retrieve the data and the scraper instance which it will
	call.
	'''
    def __init__(self, item_ids, start, scraper):
        self.item_ids = item_ids
        self.start = start
        self.scraper = scraper

    def run(self):
        for identifier in self.item_ids:
            url = f'https://api.rsbuddy.com/grandExchange?a=graph&g=30&start={self.start}&i={identifier}'
            data = scrape(self.scraper, url)
            print(f'{identifier} done')
