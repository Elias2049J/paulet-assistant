from app.application.interfaces.webscraper_interface import WebScraperInterface
from abc import ABC, abstractmethod
from typing import Any


class BaseWebScraperImpl(WebScraperInterface, ABC):
    def __init__(self, usuario: str, clave: str):
        self.usuario = usuario
        self.clave = clave

    @abstractmethod
    async def scrap(self) -> Any:
        pass