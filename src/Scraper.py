import typing
from typing import List

import socket # to resolve ip address given hostname
import urllib.parse # to parse hostname given url
import requests # to send http requests
import time # to get response time
from bs4 import BeautifulSoup # to parse the webpage
from ip2geotools.databases.noncommercial import DbIpCity # to get geolocation data
import re # for search terms

from ScrapeResult import ScrapeResult

class Scraper:

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

        links = Scraper.extract_links_from_response(soup)
        links = [urllib.parse.urljoin(self.url, link) for link in links]

        search_terms_result = Scraper.find_search_terms(soup, self.search_terms)

        return ScrapeResult(ip_address, response_time, geo_location.region, links, search_terms_result)

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

    def extract_links_from_response(soup):
        # Find all <a> tags in the parsed HTML
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and href != "#":
                links.append(href)

        return links

    def get_ip_address(url):
        try:
            parsed_url = urllib.parse.urlparse(url)
            host = parsed_url.netloc
            ip_address = socket.gethostbyname(host)
            return ip_address
        except (socket.gaierror, ValueError):
            return None

    def find_search_terms(soup, search_terms):
        result = {}
        for term in search_terms:
            result[term] = len(soup.find_all(string=re.compile(term)))
        return result

if __name__ == "__main__":
    scraper = Scraper("https://www.google.com", ["Google", "JFESE"])
    result = scraper.scrape()
    print(result)
