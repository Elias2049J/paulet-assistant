from app.infrastructure.scrapers.webscraper_base import WebScraperAdapter


class ScrappingNotas(WebScraperAdapter):
    def scrapping(self) -> str:
        return f"Notas para {self.usuario} en ciclo {self.ciclo}: 18, 19, 20 \n1. Volver a las opciones"
