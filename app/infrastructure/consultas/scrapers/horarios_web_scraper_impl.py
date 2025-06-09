# Scraper concreto para obtener horarios hardcodeados de ejemplo.
# Hereda de BaseWebScraperImpl y simula la obtención de horarios.
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl


class HorariosWebScraperImpl(BaseWebScraperImpl):
    def scrap(self) -> str:
        # Datos hardcodeados de ejemplo
        return (
            f"Horarios para {self.usuario} en ciclo {self.ciclo}:\n"
            "Lunes: Matemática 08:00-10:00 Aula 101\n"
            "Martes: Física 10:00-12:00 Aula 202\n"
            "Miércoles: Programación 14:00-16:00 Aula 303\n"
            "1. Volver a las opciones"
        )
