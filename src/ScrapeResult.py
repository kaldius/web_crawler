import typing

class ScrapeResult:

    def __init__(self):
        print('ScrapeResult initialised')

        # Response time: time from sending the request to receiving the reply
        # Data type: int/float?
        self.response_time = None

        # IP address of the server
        # Data type: str (could use ipaddress python module but lazy)
        self.server_ip = None

        # Region of the server
        # Data type: str
        self.server_region = None

        # Open ended requirement, still TBC (read assignment doc page 1)
        # Considering a dictionary mapping some search terms to their frequency of occurance
