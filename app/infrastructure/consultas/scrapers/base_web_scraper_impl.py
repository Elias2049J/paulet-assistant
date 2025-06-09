# Implementación base para scrapers web en Clean Architecture.
# Define la estructura común para los scrapers de notas y horarios.
from app.application.interfaces.webscraper_interface import WebScraperInterface
from abc import ABC, abstractmethod


class BaseWebScraperImpl(WebScraperInterface, ABC):
    def __init__(self, usuario: str, clave: str, ciclo: str):
        self.usuario = usuario  # Usuario para autenticación
        self.clave = clave      # Clave para autenticación
        self.ciclo = ciclo      # Ciclo académico

    @abstractmethod
    def scrap(self) -> str:
        # Método abstracto para realizar el scraping.
        pass
