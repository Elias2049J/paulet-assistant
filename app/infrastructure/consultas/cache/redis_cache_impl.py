# Implementación de la caché usando Redis.
# Permite almacenar y recuperar datos en Redis para cada usuario y ciclo.
from app.infrastructure.consultas.cache.base_cache_impl import BaseCacheImpl
from app.infrastructure.config.redis_client import redis_client


class RedisCacheImpl(BaseCacheImpl):
    def __init__(self, client: redis_client):
        self.redis_client = client

    def get(self, usuario: str, ciclo: str) -> str:
        # Recupera el valor desde Redis usando la clave construida.
        key = self._build_key(usuario, ciclo)
        value = self.redis_client.get(key)
        if value is not None:
            return value.decode('utf-8')
        return ""

    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        # Almacena el valor en Redis con TTL (tiempo de vida en segundos).
        key = self._build_key(usuario, ciclo)
        self.redis_client.set(key, value, ex=ttl)
