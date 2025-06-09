# Caso de uso base para consultas (notas, horarios, etc.) en Clean Architecture.
# Gestiona la obtención de datos desde caché o fuente y el guardado en caché.
from abc import ABC, abstractmethod


class BaseConsultar(ABC):
    def __init__(self, scraper, cache, usuario, ciclo):
        self.scraper = scraper  # Instancia del scraper web
        self.cache = cache      # Instancia de la caché
        self.usuario = usuario  # Usuario actual
        self.ciclo = ciclo      # Ciclo académico actual

    def obtener_de_cache(self):
        # Obtiene el resultado desde la caché.
        return self.cache.get(self.usuario, self.ciclo)

    def obtener_de_fuente(self):
        # Obtiene el resultado desde la fuente (scraper).
        return self.scraper.scrap()

    def guardar_en_cache(self, resultado):
        # Guarda el resultado en la caché con TTL de 1 hora.
        self.cache.set(self.usuario, self.ciclo, resultado, ttl=3600)

    def ejecutar_consulta(self) -> str:
        # Ejecuta la consulta: primero intenta caché, si no hay, consulta la fuente y guarda en caché.
        resultado = self.obtener_de_cache()
        if resultado:
            return f"(desde caché) {resultado}"

        resultado = self.obtener_de_fuente()
        self.guardar_en_cache(resultado)
        return f"(desde scraping) {resultado}"