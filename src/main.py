from Crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['test_search_term_1', 'test_search_term_2'],
                      3,
                      10,
                      3)
    crawler.start()
