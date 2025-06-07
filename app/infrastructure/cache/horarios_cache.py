from app.infrastructure.cache.cache_base import CacheBase


class HorariosCache(CacheBase):
    def __init__(self):
        self.store = {}

    def get(self, usuario: str, ciclo: str) -> str:
        return self.store.get(self._build_key(usuario, ciclo), "")

    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        self.store[self._build_key(usuario, ciclo)] = value
