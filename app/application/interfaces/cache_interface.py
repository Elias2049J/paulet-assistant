# Interfaz para la caché de Clean Architecture.
# Define los métodos que toda implementación de caché debe tener.
from abc import ABC, abstractmethod


class CacheInterface(ABC):
    @abstractmethod
    async def get(self, usuario: str, ciclo: str) -> str:
        # Obtiene un valor de la caché para un usuario y ciclo.
        pass

    @abstractmethod
    async def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        # Guarda un valor en la caché para un usuario y ciclo, con TTL.
        pass
