from abc import ABC, abstractmethod
from typing import Dict, Any


class CacheInterface(ABC):
    """
    Interfaz para las implementaciones de caché.
    Define el contrato que deben cumplir todas las implementaciones de caché.
    """

    @abstractmethod
    def get(self, usuario: str) -> str:
        """Obtiene un valor del caché"""
        pass

    @abstractmethod
    def set(self, usuario: str, value: str, ttl: int):
        """Establece un valor en el caché con TTL"""
        pass

    @abstractmethod
    def delete(self, usuario: str) -> bool:
        """Elimina una entrada del caché"""
        pass

    @abstractmethod
    def exists(self, usuario: str) -> bool:
        """Verifica si existe una entrada en el caché"""
        pass

    @abstractmethod
    def get_ttl(self, usuario: str) -> int:
        """Obtiene el TTL de una entrada"""
        pass

    @abstractmethod
    def clear_user_cache(self, usuario: str) -> int:
        """Limpia el caché de un usuario"""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de salud del caché"""
        pass