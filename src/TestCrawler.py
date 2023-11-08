import unittest

from Crawler import Crawler


class CrawlerTest(unittest.TestCase):
    crawler = Crawler(["lego", "businesses"],
                      2,
                      2,
                      3)

    '''
    Change inputs for self.crawler as needed. 
    Test output by checking results.json in the data folder and print statements in terminal.
    '''

    def test_crawl_url(self):
        self.crawler.start()
