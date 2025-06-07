from app.interfaces.cache_interface import CacheInterface
from abc import ABC, abstractmethod


class CacheBase(CacheInterface, ABC):
    def _build_key(self, usuario: str, ciclo: str) -> str:
        return f"{self.__class__.__name__.lower()}:{usuario}:{ciclo}"

    @abstractmethod
    def get(self, usuario: str, ciclo: str) -> str:
        pass

    @abstractmethod
    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        pass
