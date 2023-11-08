from Crawler import Crawler

if __name__ == '__main__':
    crawler = Crawler(['gpt', 'chatgpt', 'generative', 'ai'],
                      4,
                      10,
                      3)
    crawler.start()
