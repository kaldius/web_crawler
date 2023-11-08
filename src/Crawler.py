import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from Database import Database
from Scraper import Scraper

'''
Class for Crawler. Sets up threads and activates scrapers to crawl the internet, then write to file.
'''


class Crawler:
    '''
    starting_url: starting url to crawl
    search_terms: a list of terms to search for in each page scraped
    max_num_threads: the maximum number of Scraper threads to allow the Crawler to spawn 
    max_num_urls: the maximum number of urls. Once this number is hit, terminate the scraper
    '''

    def __init__(self,
                 search_terms: List[str],
                 max_num_threads: int,
                 max_num_urls: int,
                 wait_time: int):

        self.search_terms = Scraper.filter_and_lemmatize(search_terms)
        self.max_num_urls = max_num_urls
        self.max_num_threads = max_num_threads
        self.wait_time = wait_time

        self.database = Database(self.search_terms)

        self.database.load_initial_urls()

        print('Crawler initialised')

    '''
    Spawn multiple threads for Scrapers and start scraping
    '''

    def start(self):
        print(f'starting Scrapers')
        with ThreadPoolExecutor(max_workers=self.max_num_threads) as executor:
            return executor.map(self.crawl_url(), timeout=60)

    '''
    Loops while queue of urls to crawl is < max number of urls (depth limit).
    Takes out url from queue, scrapes it, adds list of new urls to queue, continues.
    Also references dictionary of visited urls to make sure (all) scraper doesn't visit same page more than once.
    Note that list of links for each result can go up to 60+ and thus file written can be very long.
    '''

    def crawl_url(self):
        while True:
            try:
                if self.database.get_no_of_scraped_url() >= self.max_num_urls:
                    print("Max URLs reached, terminate")
                    break

                url_list = self.database.get_new_url(1)

                if len(url_list) == 0:
                    print("No urls to crawl, going to sleep")
                    time.sleep(self.wait_time)
                    continue

                scraper = Scraper(url_list[0], self.search_terms)
                scraper_result = scraper.scrape()
                print("Scrape completed, inserting into database...")

                self.database.insert_scrape_result(scraper_result)

                print("Scrape result inserted into database, sleeping")
                time.sleep(self.wait_time)

            except Exception as e:
                print(f"Error crawling url: {str(e)}. Will sleep before going to next url...")
                time.sleep(self.wait_time)
