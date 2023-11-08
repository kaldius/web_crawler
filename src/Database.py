from typing import List
import os
import threading
import json
from collections import deque

mutexLock = threading.Lock()

from ScrapeResult import ScrapeResult

# NOTE: there might be a chance tha multiple threads attempt to write to the DataBase
# at the same time, so proper access-lock mechanism needs to be implemented
class Database:
    dirname = os.path.dirname(__file__)
    storage_directory = os.path.join(dirname, '../data/')
    initial_urls_file = os.path.join(storage_directory, 'initialUrls.txt')
    results_file = os.path.join(storage_directory, 'results.json')
    frequencies_file = os.path.join(storage_directory, 'frequencies.json')

    def __init__(self, search_terms):
        print('Database initialised')
        if not os.path.exists(self.storage_directory):
            print(f'Error: data directory does not exist')
            exit(1)
        initialUrls = self.load_initial_urls()
        self.results = {
            'scrapedUrls': {},
            'unscrapedUrls': initialUrls,
            'urlsBeingScraped': set()
        }
        # keeps a running value of the frequencies, so we don't have to extract from
        # the large json file later
        self.search_term_frequency = {term: 0 for term in search_terms}

    def isInitialUrlsFileAvailable(self) -> bool:
        return os.path.exists(self.initial_urls_file)

    def load_initial_urls(self):
        if not self.isInitialUrlsFileAvailable():
            print(f'Initial urls file {self.initial_urls_file} not found in data directory')
            exit(1)
        with open(self.initial_urls_file, 'r') as file:
            initialUrls = deque([line.strip() for line in file.readlines()])
            return initialUrls

    def get_new_url(self, num_urls: int = 1) -> List[str]:
        urls = []
        with mutexLock:
            for i in range(num_urls):
                if not self.results['unscrapedUrls']:
                    break
                new_url = self.results['unscrapedUrls'].popleft()
                self.results['urlsBeingScraped'].add(new_url)
                urls.append(new_url)
        return urls

    def get_no_of_scraped_url(self):
        with mutexLock:
            size = len(self.results['scrapedUrls']) + len(self.results['urlsBeingScraped'])
        return size

    def insert_scrape_result(self, result: ScrapeResult) -> None:
        self.results['urlsBeingScraped'].discard(result.url)
        self.results['scrapedUrls'][result.url] = result.__dict__
        with mutexLock:
            self.update_search_term_frequency(result.search_terms_result)
            with open(self.results_file, 'w') as resultsFile:
                resultsFile.write(json.dumps(self.results['scrapedUrls']))
                for link in result.links:
                    if link not in self.results['scrapedUrls'] and link not in self.results['unscrapedUrls'] and link not in self.results['urlsBeingScraped']:
                        self.results['unscrapedUrls'].append(link)

    def update_search_term_frequency(self, result: dict):
        for k in self.search_term_frequency.keys():
            if k not in result:
                continue
            self.search_term_frequency[k] += result[k]
        with open(self.frequencies_file, 'w') as frequenciesFile:
            frequenciesFile.write(json.dumps(self.search_term_frequency))