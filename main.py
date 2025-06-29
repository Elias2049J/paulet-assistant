import os
import logging
import threading
import time
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
from app.infrastructure.presenters.chatbot_presenter import ChatbotPresenter
from app.infrastructure.routes.chatbot_routes import get_router
from app.infrastructure.routes.cache_routes import get_cache_router
from app.infrastructure.routes.monitoring_routes import router as monitoring_router
from app.infrastructure.monitoring.system_monitor import SystemMonitor
from app.infrastructure.config.redis_config import redis_config
from dotenv import load_dotenv


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


# Monitoreo de memoria
def monitor_memory():
    while True:
        SystemMonitor.log_system_resources()
        time.sleep(10)


threading.Thread(target=monitor_memory, daemon=True).start()

# Cargar variables de entorno
load_dotenv()

# Configurar logging en terminal
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar dependencias
try:
    # Cliente Redis
    redis = redis_client()
    logger.info("Cliente Redis configurado exitosamente")

    # Implementaciones de caché
    cache_impl = RedisCacheImpl(redis)

    # Inicializar scrapers y casos de uso con None
    notas_scraper = CalificacionPlaywrightScraperImpl(None, None, redis)
    horarios_scraper = HorariosWebScraperImpl(None, None, redis)

    consultar_notas_uc = ConsultarNotasUseCase(notas_scraper, cache_impl, None)
    consultar_horarios_uc = ConsultarHorariosUseCase(horarios_scraper, cache_impl, None)

    use_cases = {
        "consultar_notas": consultar_notas_uc,
        "consultar_horarios": consultar_horarios_uc
    }

    menus = MenuLoader.load_from_file("app/infrastructure/config/menus_config.json")
    chatbot_service = ChatbotService(menus, use_cases)
    chatbot_presenter = ChatbotPresenter(chatbot_service)
    chatbot_router = get_router(chatbot_presenter, redis=redis)
    cache_router = get_cache_router(cache_impl)

    app.include_router(chatbot_router, tags=["Chatbot"])
    app.include_router(cache_router, prefix="/admin", tags=["Cache Administration"])
    app.include_router(monitoring_router, prefix="/admin/monitoring", tags=["Monitoring"])

    logger.info("Todas las dependencias configuradas exitosamente")

except Exception as e:
    logger.error(f"Error durante la configuración de la aplicación: {e}")
    raise


@app.get("/")
async def root():
    return {
        "message": "Paulet Assistant API está funcionando",
        "version": "1.0.0",
        "arquitectura": "Servicio chatbot con sistema de menús",
        "endpoints": {
            "chat": "/paulet/chat",
            "cache_health": "/admin/cache/health",
            "cache_stats": "/admin/cache/stats",
            "monitoring": "/admin/monitoring"
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
                "usuario": redis.get("USUARIO") or None,
                "arquitectura": "Chatbot con menús"
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
