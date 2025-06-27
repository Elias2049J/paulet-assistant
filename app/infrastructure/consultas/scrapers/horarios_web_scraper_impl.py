# Scraper concreto para obtener horarios hardcodeados de ejemplo.
# Hereda de BaseWebScraperImpl y simula la obtención de horarios.
from app.infrastructure.consultas.scrapers.base_web_scraper_impl import BaseWebScraperImpl


class HorariosWebScraperImpl(BaseWebScraperImpl):
    def scrap(self) -> dict:
        # Datos hardcodeados de ejemplo
        return {
            "Lunes": [
                {"curso": "Matemática", "desde": "08:00", "hasta": "10:00", "sede": "Aula 101"}
            ],
            "Martes": [
                {"curso": "Física", "desde": "10:00", "hasta": "12:00", "sede": "Aula 202"}
            ],
            "Miércoles": [
                {"curso": "Programación", "desde": "14:00", "hasta": "16:00", "sede": "Aula 303"}
            ]
        }
