import typing
import json 

class ScrapeResult:

    def __init__(self, url, ip_address, response_time, region, links, search_terms_result):
        print('ScrapeResult initialised')

        # URL of the page
        # Data type: str
        self.url = url

        # IP address of the server
        # Data type: str
        self.server_ip = ip_address

        # Response time: time from sending the request to receiving the reply
        # Data type: float
        self.response_time = response_time

        # Region of the server
        # Data type: str
        self.server_region = region

        # Links found in the html
        # Data type: list[str]
        self.links = links

        # Open ended requirement, still TBC (read assignment doc page 1)
        # Considering a dictionary mapping some search terms to their frequency of occurance
        self.search_terms_result = search_terms_result

    def get_links(self):
        return self.links

    def __str__(self):
        first = (f"IP Address: {self.server_ip}\n"
                f"Response Time: {self.response_time}\n"
                f"Server Region: {self.server_region}")
        second = "Links:\n" + "\n".join(self.links)
        third = json.dumps(self.search_terms_result)
        return "\n".join([first, second, third])