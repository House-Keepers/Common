from abc import ABC, abstractmethod


class BaseBot(ABC):
    def __init__(self, api_url: str = None):
        """
        Starts by initialize a session url
        :param api_url: API url for the channel
        """
        self.api_url = api_url

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def parse_format(self):
        pass

    @abstractmethod
    def post(self, where: str, **kwargs):
        pass
