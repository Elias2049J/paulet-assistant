from app.interfaces.webscraper_interface import WebScraperInterface
from abc import ABC, abstractmethod


class WebScraperAdapter(WebScraperInterface, ABC):
    def __init__(self, usuario: str, clave: str, ciclo: str):
        self.usuario = usuario
        self.clave = clave
        self.ciclo = ciclo

    @abstractmethod
    def scrapping(self) -> str:
        pass
