import typing
from typing import List

from ScrapeResult import ScrapeResult

# NOTE: there might be a chance tha multiple threads attempt to write to the DataBase
# at the same time, so proper access-lock mechanism needs to be implemented
class Database:

    def __init__(self, storage_dir: str = '../data/'):
        # go to storage_dir and load in the files there
        # put data in '../data/' by default?
        print('Database initialised')
        pass

    def get_new_url(self, num_urls: int = 1) -> List[str]:
        # look for a url that has not been scraped and return it as a string
        # if num_urls specified, return that number of urls
        # if number of available urls < num_urls, just return as many as possible
        print(f'Getting {num_urls} urls from the database')
        pass

    def insert_scrape_result(self, result: ScrapeResult) -> None:
        # insert the results into the db
        print('Inserting scrape result into database')
        pass
