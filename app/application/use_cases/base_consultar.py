# Caso de uso base para consultas (notas, horarios, etc.) en Clean Architecture.
# Gestiona la obtención de datos desde caché o fuente y el guardado en caché.
from abc import ABC, abstractmethod
import asyncio
import inspect


class BaseConsultar(ABC):
    def __init__(self, scraper, cache, usuario, ciclo):
        self.scraper = scraper  # Instancia del scraper web
        self.cache = cache      # Instancia de la caché
        self.usuario = usuario  # Usuario actual
        self.ciclo = ciclo      # Ciclo académico actual

    def obtener_de_cache(self):
        # obtiene resultado desde caché
        return self.cache.get(self.usuario, self.ciclo)

    def obtener_de_fuente(self):
        # obtiene el resultado desde la fuente (scraping)
        metodo_scrap = self.scraper.scrap
        if inspect.iscoroutinefunction(metodo_scrap):
            return asyncio.run(metodo_scrap())
        return metodo_scrap()

    def guardar_en_cache(self, resultado):
        # guarda el resultado caché con TTL de 1 hora
        self.cache.set(self.usuario, self.ciclo, resultado, ttl=3600)

    @abstractmethod
    def ejecutar_consulta(self):
        # debe ser implementado por los casos de uso concretos para devolver datos estructurados
        pass
