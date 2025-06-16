# Interfaz para los scrapers web en Clean Architecture.
# Define el método que debe implementar cualquier scraper.

from abc import ABC, abstractmethod


class WebScraperInterface(ABC):
    @abstractmethod
    async def scrap(self) -> str:
        # Realiza el scraping y retorna los datos como string.
        pass
