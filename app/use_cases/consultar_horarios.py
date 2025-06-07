from app.infrastructure.scrapers.scrapping_horarios import ScrappingHorarios
from app.infrastructure.cache.horarios_cache import HorariosCache


class ConsultarHorariosUseCase:
    def __init__(self, usuario: str, clave: str, ciclo: str):
        self.scraper = ScrappingHorarios(usuario, clave, ciclo)
        self.cache = HorariosCache()
        self.usuario = usuario
        self.ciclo = ciclo

    def ejecutar(self) -> str:
        resultado = self.cache.get(self.usuario, self.ciclo)
        if resultado:
            return f"(desde caché) {resultado}"

        # Aquí se ejecutaría el scraping real con Playwright (login, navegación, extracción, parseo)
        resultado = self.scraper.scrapping()

        self.cache.set(self.usuario, self.ciclo, resultado, ttl=3600)
        return f"(desde scraping) {resultado}"
