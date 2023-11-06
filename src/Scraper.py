import typing
from typing import List

import socket # to resolve ip address given hostname
import urllib.parse # to parse hostname given url
import requests # to send http requests
import time # to get response time
from bs4 import BeautifulSoup # to parse the webpage
from ip2geotools.databases.noncommercial import DbIpCity
# from geopy.distance import distance

from ScrapeResult import ScrapeResult

class Scraper:

    def __init__(self, url: str, search_terms: List[str]):
        print('Scraper initialised')
        self.url = url
        self.search_terms = search_terms

    def scrape(self) -> ScrapeResult:
        print('Scraper scraping')

        ip_address = Scraper.get_ip_address(self.url)
        if not ip_address:
            print("Failed to resolve ip address")
            return None

        tmp = Scraper.send_html_request(self.url)
        if not tmp:
            print("Failed to send html request")
            return None
        
        response = tmp[0]
        response_time = tmp[1]

        geo_location = DbIpCity.get(ip_address, api_key="free")

        links = Scraper.extract_links_from_response(response)
        links = [urllib.parse.urljoin(self.url, link) for link in links]

        return ScrapeResult(ip_address, response_time, geo_location.region, links)
        # send the necessary http requests,
        # parse http response and search for search_terms and their frequency of occurance,
        # get geolocation data,
        # put all the data into a ScrapeResult and return it
    
    def send_html_request(url):
        try:
            # Send an HTTP GET request to the specified URL
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

    def extract_links_from_response(response):
        soup = BeautifulSoup(response.text, 'html.parser')

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


scraper = Scraper("https://www.mit.edu", [])
result = scraper.scrape()
print(result)