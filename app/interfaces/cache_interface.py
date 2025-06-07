from abc import ABC, abstractmethod


class CacheInterface(ABC):
    @abstractmethod
    def get(self, usuario: str, ciclo: str) -> str:
        pass

    @abstractmethod
    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        pass
