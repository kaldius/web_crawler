import typing
from typing import List

from ScrapeResult import ScrapeResult
from Database import Database
from Scraper import Scraper

class Crawler:
    
    '''
    starting_url: obvious
    search_terms: a list of terms to search for in each page scraped
    max_num_threads: the maximum number of Scraper threads to allow the Crawler to spawn 
    max_num_urls: the maximum number of urls. Once this number is hit, terminate the scraper
    '''
    def __init__(self,
                 starting_url: str,
                 search_terms: List[str],
                 max_num_threads: int,
                 max_num_urls: int):
        print('Crawler initialised')
        pass

    def start(self):
        # spawn multiple threads for Scrapers and start scraping
        # once scraper.scrape() returns, write the data to the database
        print(f'starting Scrapers')
        pass

