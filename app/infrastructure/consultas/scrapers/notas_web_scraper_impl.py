# Scraper concreto para obtener notas hardcodeadas de ejemplo.
# Hereda de BaseWebScraperImpl y simula la obtención de notas.
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl


class NotasWebScraperImpl(BaseWebScraperImpl):
    def scrap(self) -> str:
        # Datos hardcodeados de ejemplo
        return (
            f"Notas para {self.usuario} en ciclo {self.ciclo}:\n"
            "- Matemática: 18 (faltas: 1/5)\n"
            "- Física: 19 (faltas: 0/5)\n"
            "- Programación: 20 (faltas: 2/5)\n"
            "1. Volver a las opciones"
        )
