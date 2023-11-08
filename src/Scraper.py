import socket  # to resolve ip address given hostname
import time  # to get response time
import urllib.parse  # to parse hostname given url
from typing import List

import requests  # to send http requests
import spacy  # to convert words to canonical form
from bs4 import BeautifulSoup  # to parse the webpage
from ip2geotools.databases.noncommercial import DbIpCity  # to get geolocation data

from ScrapeResult import ScrapeResult


class Scraper:
    lemmatizer = spacy.load("en_core_web_sm")

    def __init__(self, url: str, search_terms: List[str]):
        print('Scraper initialised')
        self.url = url
        self.search_terms = search_terms

    # send the necessary http requests,
    # parse http response and search for search_terms and their frequency of occurance,
    # get geolocation data,
    # put all the data into a ScrapeResult and return it
    # returns None if anything fails
    def scrape(self) -> ScrapeResult:
        print('Scraper scraping')

        ip_address = Scraper.get_ip_address(self.url)
        if not ip_address:
            print("Failed to resolve ip address")
            return None

        geo_location = DbIpCity.get(ip_address, api_key="free")

        tmp = Scraper.send_html_request(self.url)
        if not tmp:
            print("Failed to send html request")
            return None

        response, response_time = tmp

        soup = BeautifulSoup(response.text, 'html.parser')

        links = Scraper.extract_links_from_response(soup, self.url)

        search_terms_result = Scraper.find_search_terms(soup, self.search_terms)

        return ScrapeResult(self.url, ip_address, response_time, geo_location.region, links, search_terms_result)

    def send_html_request(url):
        # Send an HTTP GET request to the specified URL
        try:
            start_time = time.time()
            response = requests.get(url, timeout=5)
            end_time = time.time()
            if response.status_code == 200:
                response_time = end_time - start_time
                return (response, response_time)
            else:
                print(f"HTTP GET request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None

    def extract_links_from_response(soup, base_url):
        # Find all <a> tags in the parsed HTML
        links = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href != "#":
                remove_fragment = urllib.parse.urlparse(href)._replace(fragment="").geturl()
                absolute_url = urllib.parse.urljoin(base_url, remove_fragment)
                links.add(absolute_url)

        return list(links)

    def get_ip_address(url):
        try:
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.netloc
            ip_address = socket.gethostbyname(host)
            return ip_address
        except (socket.gaierror, ValueError):
            return None

    def find_search_terms(soup, search_terms: List[str]):
        texts = soup.get_text().split()

        lemmatized_words = Scraper.filter_and_lemmatize(texts)
        lemmatized_search_terms = Scraper.filter_and_lemmatize(search_terms)

        result = {term: lemmatized_words.count(term) for term in set(lemmatized_search_terms)}

        return result

    def filter_and_lemmatize(words: List[str]):
        lowered_ascii_words = [word.lower() for word in words if word.isascii()]
        filtered_words = [word for word in lowered_ascii_words if not (word.isnumeric() or not word.isalpha())]
        return [token.lemma_ for word in filtered_words for token in Scraper.lemmatizer(word)]


if __name__ == "__main__":
    scraper = Scraper("https://en.wikipedia.org/wiki/Lego",
                      ["LeGo", "legos", "businesses", "bUsineSS", "games", "game"])
    result = scraper.scrape()
    print(result)
