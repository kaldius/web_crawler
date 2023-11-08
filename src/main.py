from Crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['rejection', 'depression', 'jobless', 'competitive', 'retrench', 'recind', 'layoff', 'termination', 'dismiss', 'severance'],
                      4,
                      10,
                      3)
    crawler.start()
