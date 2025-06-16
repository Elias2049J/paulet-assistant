# Punto de entrada principal de la aplicacion
# Configura el flujo de la app: rutas, casos de uso, scrapers, caché y servicios.
import os

from fastapi import FastAPI
from app.infrastructure.routes.chatbot_routes import get_router
from app.domain.entities.decision_tree import DecisionTree
from app.application.use_cases.consultar_notas_use_case import ConsultarNotasUseCase
from app.application.use_cases.consultar_horarios_use_case import ConsultarHorariosUseCase
from app.infrastructure.consultas.scrapers.notas_playwright_scraper_impl import NotasPlaywrightScraperImpl
from app.infrastructure.consultas.cache.redis_cache_impl import RedisCacheImpl
from app.infrastructure.consultas.scrapers.horarios_web_scraper_impl import HorariosWebScraperImpl
from app.application.services.chatbot_service import ChatbotService
from app.application.services.flow_manager_service import FlowManagerService
from app.infrastructure.presenters.chatbot_presenter import ChatbotPresenter
from app.infrastructure.config.redis_client import redis_client
from app.infrastructure.config.cors_config import configure_cors

# Configuración de la app y CORS
app = FastAPI()
configure_cors(app)

# Datos fijos para el usuario de pruebas
usuario = os.getenv("USUARIO")
clave = os.getenv("PASSWORD")
ciclo = "2025-1"

# Variables globales para dependencias
redis_cache = RedisCacheImpl(redis_client())
use_cases = {
    "consultar_notas": ConsultarNotasUseCase(
        NotasPlaywrightScraperImpl(usuario, clave, ciclo), redis_cache, usuario, ciclo
    ),
    "consultar_horarios": ConsultarHorariosUseCase(
        HorariosWebScraperImpl(usuario, clave, ciclo), redis_cache, usuario, ciclo
    )
}
flow_manager = FlowManagerService(DecisionTree())
chatbot_service = ChatbotService(flow_manager, use_cases)
controller = ChatbotPresenter(chatbot_service)
app.include_router(get_router(controller))
