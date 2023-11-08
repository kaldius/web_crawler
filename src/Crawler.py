import time
from typing import List
from concurrent.futures import ThreadPoolExecutor
import threading

from ScrapeResult import ScrapeResult
from Scraper import Scraper

'''
Class for Crawler. Sets up threads and activates scrapers to crawl the internet, then write to file.
'''
class Crawler:
    starting_url = None
    search_terms = None
    max_num_threads = None
    max_num_urls = None
    url_counter = 0
    wait_time = None
    thread_lock = threading.Lock()
    queue = []
    visited_urls = {}

    '''
    starting_url: starting url to crawl
    search_terms: a list of terms to search for in each page scraped
    max_num_threads: the maximum number of Scraper threads to allow the Crawler to spawn 
    max_num_urls: the maximum number of urls. Once this number is hit, terminate the scraper
    '''
    def __init__(self,
                 starting_url: str,
                 search_terms: List[str],
                 max_num_threads: int,
                 max_num_urls: int,
                 wait_time: int):

        self.starting_url = starting_url
        self.search_terms = search_terms
        self.max_num_urls = max_num_urls
        self.max_num_threads = max_num_threads
        self.wait_time = wait_time

        print('Crawler initialised')

    '''
    Spawn multiple threads for Scrapers and start scraping
    '''
    def start(self):
        print(f'starting Scrapers')
        self.queue.append(self.starting_url)
        with ThreadPoolExecutor(max_workers=self.max_num_threads) as executor:
            return executor.map(self.crawl_url(), timeout=60)

    '''
    Loops while queue of urls to crawl is < max number of urls (depth limit).
    Takes out url from queue, scrapes it, adds list of new urls to queue, continues.
    Also references dictionary of visited urls to make sure (all) scraper doesn't visit same page more than once.
    Note that list of links for each result can go up to 60+ and thus file written can be very long.
    '''
    def crawl_url(self):
        try:
            while self.url_counter < self.max_num_urls:
                if len(self.queue) == 0:
                    print("No urls to crawl, going to sleep")
                    time.sleep(self.wait_time)
                    continue

                self.thread_lock.acquire()
                url = self.queue.pop(0)
                self.thread_lock.release()

                if url in self.visited_urls:
                    continue

                scraper = Scraper(url, self.search_terms)
                scraper_result = scraper.scrape()

                self.thread_lock.acquire()
                self.queue.extend(scraper_result.get_links())
                self.url_counter += 1
                self.write_to_file(scraper_result)
                self.visited_urls[url] = 1
                self.thread_lock.release()

                print("Write to file done, going to sleep")
                time.sleep(self.wait_time)

        except Exception as e:
            print(f"Error crawling: {str(e)}")

        print("Max URLs reached, terminate")

    '''
    Writes results to file scrape_results.txt in data folder.
    '''
    def write_to_file(self, scrape_result: ScrapeResult):
        with open("../data/scrape_results.txt", "a") as f:
            f.write(f"Result {self.url_counter}:\n" + str(scrape_result) + "\n")

