import typing
from typing import List

from ScrapeResult import ScrapeResult

class Scraper:

    def __init__(self, url: str, search_terms: List[str]):
        print('Scraper initialised')
        pass

    def scrape(self) -> ScrapeResult:
        print('Scraper scraping')
        # send the necessary http requests,
        # parse http response and search for search_terms and their frequency of occurance,
        # get geolocation data,
        # put all the data into a ScrapeResult and return it
        pass
