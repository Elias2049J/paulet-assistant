from app.infrastructure.scrapers.webscraper_base import WebScraperAdapter


class ScrappingHorarios(WebScraperAdapter):
    def scrapping(self) -> str:
        return f"Horarios para {self.usuario} en ciclo {self.ciclo}: Lunes y Martes\n1. Volver a las opciones"
