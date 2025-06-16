# Implementación base para la caché en Clean Architecture.
# Proporciona la construcción de claves y define la interfaz para get/set.
from app.application.interfaces.cache_interface import CacheInterface
from abc import ABC, abstractmethod


class BaseCacheImpl(CacheInterface, ABC):
    def _build_key(self, usuario: str, ciclo: str) -> str:
        # Construye una clave única para la caché según usuario y ciclo.
        return f"{self.__class__.__name__.lower()}:{usuario}:{ciclo}"

    @abstractmethod
    async def get(self, usuario: str, ciclo: str) -> str:
        pass

    @abstractmethod
    async def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        pass
