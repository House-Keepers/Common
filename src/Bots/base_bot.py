from abc import ABC, abstractmethod


class BaseBot(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def run(self, **kwargs):
        pass
