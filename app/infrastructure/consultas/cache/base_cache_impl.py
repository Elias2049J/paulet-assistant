# Implementación base para la caché en Clean Architecture.
# Proporciona la construcción de claves y define la interfaz para get/set.
from app.application.interfaces.cache_interface import CacheInterface
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseCacheImpl(CacheInterface, ABC):
    def _build_key(self, usuario: str, ciclo: str) -> str:
        # Construye una clave única para la caché según usuario y ciclo.
        return f"{self.__class__.__name__.lower()}:{usuario}:{ciclo}"

    @abstractmethod
    def get(self, usuario: str, ciclo: str) -> str:
        pass

    @abstractmethod
    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        pass

    @abstractmethod
    def delete(self, usuario: str, ciclo: str) -> bool:
        pass

    @abstractmethod
    def exists(self, usuario: str, ciclo: str) -> bool:
        pass

    @abstractmethod
    def get_ttl(self, usuario: str, ciclo: str) -> int:
        pass

    @abstractmethod
    def clear_user_cache(self, usuario: str) -> int:
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        pass
