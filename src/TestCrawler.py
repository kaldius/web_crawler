from Crawler import Crawler
from ScrapeResult import ScrapeResult
import unittest
from unittest.mock import mock_open, patch

class CrawlerTest(unittest.TestCase):

    crawler = Crawler("https://en.wikipedia.org/wiki/Lego",
                      ["lego", "businesses"],
                      2,
                      2,
                      3)

    '''
    Change inputs for self.crawler as needed. Test output in scrape_results.txt in the data folder and print statements in terminal.
    '''
    def test_crawl_url(self):
        self.crawler.start()


    def test_scrape_result(self):
        self.crawler.url_counter = 1
        scrape_result = ScrapeResult("https://nusit.nus.edu.sg/",
                                     "137.132.60.0",
                                     0.0,
                                     "Singapore",
                                     ["https://nusit.nus.edu.sg/about/", "https://nusit.nus.edu.sg/contact/"],
                                     {"about": 1, "contact": 2})

        with patch('builtins.open', mock_open()) as m:
            self.crawler.write_to_file(scrape_result)
            m.assert_called_once_with("../data/scrape_results.txt", "a")
            m().write.assert_called_once_with("Result 1:\n" + str(scrape_result) + "\n")
