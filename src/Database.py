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

    def __init__(self):
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

    def insert_scrape_result(self, result: ScrapeResult) -> None:
        self.results['urlsBeingScraped'].discard(result.url)
        self.results['scrapedUrls'][result.url] = result.__dict__
        with mutexLock:
            with open(self.results_file, 'w') as resultsFile:
                resultsFile.write(json.dumps(self.results['scrapedUrls']))
                for link in result.links:
                    if link not in self.results['scrapedUrls'] and link not in self.results['unscrapedUrls'] and link not in self.results['urlsBeingScraped']:
                        self.results['unscrapedUrls'].append(link)
