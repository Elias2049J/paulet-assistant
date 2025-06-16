# Implementación de la caché usando Redis.
# Permite almacenar y recuperar datos en Redis para cada usuario y ciclo.
from app.infrastructure.consultas.cache.base_cache_impl import BaseCacheImpl
from app.infrastructure.config.redis_client import redis_client


class RedisCacheImpl(BaseCacheImpl):
    def __init__(self, client: redis_client):
        self.redis_client = client

    async def get(self, usuario: str, ciclo: str) -> str:
        # recupera el valor desde Redis usando la clave construida.
        key = self._build_key(usuario, ciclo)
        value = await self.redis_client.get(key)
        return value if value is not None else ""

    async def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        # almacena el valor en Redis con TTL
        key = self._build_key(usuario, ciclo)
        await self.redis_client.set(key, value, ex=ttl)
