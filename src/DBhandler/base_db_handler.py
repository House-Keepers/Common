from abc import ABC, abstractmethod
from pymongo import MongoClient


class BaseDBHandler(ABC):
    def __init__(self, connection_string: str, max_pool_size: int):
        """
        Starts by initialize a session url
        :param api_url: API url for the channel
        """
        self.connection_string = connection_string
        self.max_pool_size = max_pool_size

    def connect(self):
        return MongoClient(host=self.connection_string, maxPoolSize=self.max_pool_size)

    @abstractmethod
    def query(self):
        pass

    @abstractmethod
    def insert(self, documents: list):
        pass
