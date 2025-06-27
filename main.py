import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.infrastructure.config.cors_config import configure_cors
from app.infrastructure.config.redis_client import redis_client
from app.infrastructure.config.menu_loader import MenuLoader
from app.infrastructure.consultas.cache.redis_cache_impl import RedisCacheImpl
from app.infrastructure.consultas.scrapers.calificacion_playwright_scraper_impl import CalificacionPlaywrightScraperImpl
from app.infrastructure.consultas.scrapers.horarios_web_scraper_impl import HorariosWebScraperImpl
from app.application.use_cases.consultar_notas_use_case import ConsultarNotasUseCase
from app.application.use_cases.consultar_horarios_use_case import ConsultarHorariosUseCase
from app.application.services.chatbot_service import ChatbotService
from app.application.services.conversation_state_service import ConversationStateService
from app.infrastructure.presenters.chatbot_presenter import ChatbotPresenter
from app.infrastructure.routes.chatbot_routes import get_router
from app.infrastructure.routes.cache_routes import get_cache_router
from app.infrastructure.config.redis_config import redis_config
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación Paulet Assistant")
    logger.info(f"Configuración Redis: {redis_config.host}:{redis_config.port}")
    yield
    logger.info("Cerrando aplicación Paulet Assistant")

# Crear aplicación FastAPI
app = FastAPI(
    title="Paulet Assistant API",
    description="API del asistente virtual Paulet para consultas académicas",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
configure_cors(app)

# Configurar dependencias
try:
    # Cliente Redis
    redis = redis_client()
    logger.info("Cliente Redis configurado exitosamente")

    # Implementaciones de caché
    cache_impl = RedisCacheImpl(redis)

    # Obtener credenciales de variables de entorno (obligatorias)
    usuario = os.getenv("USUARIO")
    password = os.getenv("PASSWORD")

    if not usuario or not password:
        logger.error("Error: las credenciales USUARIO y PASSWORD deben estar definidas en el archivo .env")
        raise ValueError("faltan credenciales en el .env")

    ciclo = "2025-1"

    # Scrapers
    notas_scraper = CalificacionPlaywrightScraperImpl(usuario, password, ciclo)
    horarios_scraper = HorariosWebScraperImpl(usuario, password, ciclo)

    # Casos de uso
    consultar_notas_uc = ConsultarNotasUseCase(notas_scraper, cache_impl, usuario, ciclo)
    consultar_horarios_uc = ConsultarHorariosUseCase(horarios_scraper, cache_impl, usuario, ciclo)

    # Diccionario de casos de uso
    use_cases = {
        "consultar_notas": consultar_notas_uc,
        "consultar_horarios": consultar_horarios_uc
    }

    # Cargar configuración de menús
    menus = MenuLoader.load_from_file("menus_config.json")

    # Servicios (usando el nuevo servicio unificado)
    chatbot_service = ChatbotService(menus, use_cases)

    # Presenter
    chatbot_presenter = ChatbotPresenter(chatbot_service)

    # Registrar rutas
    chatbot_router = get_router(chatbot_presenter)
    cache_router = get_cache_router(cache_impl)

    app.include_router(chatbot_router, tags=["Chatbot"])
    app.include_router(cache_router, prefix="/admin", tags=["Cache Administration"])

    logger.info("Todas las dependencias configuradas exitosamente")

except Exception as e:
    logger.error(f"Error durante la configuración de la aplicación: {e}")
    raise

@app.get("/")
async def root():
    return {
        "message": "Paulet Assistant API está funcionando",
        "version": "1.0.0",
        "arquitectura": "Servicio chatbot unificado con sistema de menús simplificado",
        "endpoints": {
            "chat": "/paulet/chat",
            "cache_health": "/admin/cache/health",
            "cache_stats": "/admin/cache/stats"
        }
    }

@app.get("/health")
async def health_check():
    try:
        cache_health = cache_impl.health_check()
        return {
            "status": "healthy",
            "cache": cache_health,
            "configuration": {
                "redis_host": redis_config.host,
                "redis_port": redis_config.port,
                "usuario": usuario,
                "arquitectura": "Chatbot unificado con menús simplificados"
            }
        }
    except Exception as e:
        logger.error(f"Error en health check: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )