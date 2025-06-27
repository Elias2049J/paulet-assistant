# Interfaz para los scrapers web en Clean Architecture.
# Define el método que debe implementar cualquier scraper.

from abc import ABC, abstractmethod
from typing import Any


class WebScraperInterface(ABC):
    @abstractmethod
    def scrap(self) -> Any:
        # Realiza el scraping y retorna los datos como string.
        pass
