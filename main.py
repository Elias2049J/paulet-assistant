# Punto de entrada principal de la aplicación FastAPI para el backend de Paulet Assistant.
# Configura el flujo de Clean Architecture: rutas, casos de uso, scrapers, caché y servicios.
from fastapi import FastAPI
from app.infrastructure.routes.chatbot_routes import get_router
from app.domain.entities.decision_tree import DecisionTree
from app.application.use_cases.consultar_notas_use_case import ConsultarNotasUseCase
from app.application.use_cases.consultar_horarios_use_case import ConsultarHorariosUseCase
from app.infrastructure.consultas.scrapers.notas_web_scraper_impl import NotasWebScraperImpl
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

# Datos fijos para el usuario de pruebas (ajustar si se requiere multiusuario)
usuario = "usuario_demo"
clave = "123456"
ciclo = "2025-1"

# Instancia de caché Redis
cache = RedisCacheImpl(redis_client)

# Casos de uso con scrapers y caché, para notas y horarios
use_cases = {
    "consultar_notas": ConsultarNotasUseCase(
        NotasWebScraperImpl(usuario, clave, ciclo), cache, usuario, ciclo
    ),
    "consultar_horarios": ConsultarHorariosUseCase(
        HorariosWebScraperImpl(usuario, clave, ciclo), cache, usuario, ciclo
    )
}

# Configuración del flujo conversacional y servicios
flow_manager = FlowManagerService(DecisionTree())
chatbot_service = ChatbotService(flow_manager, use_cases)
controller = ChatbotPresenter(chatbot_service)

# Registro de la ruta principal del chatbot
app.include_router(get_router(controller))
