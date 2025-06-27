from abc import ABC, abstractmethod
from typing import Any


class WebScraperInterface(ABC):
    @abstractmethod
    async def scrap(self) -> Any:
        pass
    