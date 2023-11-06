import typing

class ScrapeResult:

    def __init__(self, ip_address, response_time, links):
        print('ScrapeResult initialised')

        # IP address of the server
        # Data type: str
        self.server_ip = ip_address

        # Response time: time from sending the request to receiving the reply
        # Data type: float
        self.response_time = response_time

        # Region of the server
        # Data type: str TODO
        self.server_region = None

        # Links found in the html
        # Data type: list of str
        self.links = links

        # Open ended requirement, still TBC (read assignment doc page 1)
        # Considering a dictionary mapping some search terms to their frequency of occurance
