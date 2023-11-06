import typing

class ScrapeResult:

    def __init__(self, ip_address, response_time, region, links):
        print('ScrapeResult initialised')

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
        # Data type: list of str
        self.links = links

        # Open ended requirement, still TBC (read assignment doc page 1)
        # Considering a dictionary mapping some search terms to their frequency of occurance
    
    def __str__(self):
        first = (f"IP Address: {self.server_ip}\n"
                f"Response Time: {self.response_time}\n"
                f"Server Region: {self.server_region}\n"
                f"Links:\n")
        return first + "\n".join(self.links)