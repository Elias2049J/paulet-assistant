from abc import ABC, abstractmethod


class WebScraperInterface(ABC):
    @abstractmethod
    def scrapping(self) -> str:
        pass
