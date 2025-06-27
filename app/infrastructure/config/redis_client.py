# Configuración del cliente Redis para la caché de la aplicación.
# Permite la conexión a Redis usando variables de entorno o valores por defecto.
from redis import Redis, ConnectionPool
from redis.exceptions import ConnectionError, TimeoutError
import os
import logging
from app.infrastructure.config.redis_config import redis_config

logger = logging.getLogger(__name__)

def redis_client():
    """
    Crea una instancia del cliente Redis con configuración robusta
    y manejo de errores.
    """
    try:
        # Configuración del pool de conexiones usando la config centralizada
        connection_pool = ConnectionPool(
            host=redis_config.host,
            port=redis_config.port,
            db=redis_config.db,
            password=redis_config.password,
            max_connections=redis_config.max_connections,
            socket_timeout=redis_config.socket_timeout,
            socket_connect_timeout=redis_config.socket_connect_timeout,
            encoding="utf-8",
            decode_responses=True,
            retry_on_timeout=redis_config.retry_on_timeout,
            health_check_interval=redis_config.health_check_interval
        )

        # Crear cliente Redis
        client = Redis(connection_pool=connection_pool)

        # Verificar conexión
        client.ping()
        logger.info(f"Conexión a Redis establecida exitosamente en {redis_config.host}:{redis_config.port}")

        return client

    except (ConnectionError, TimeoutError) as e:
        logger.error(f"Error al conectar con Redis: {e}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al configurar Redis: {e}")
        raise

def get_redis_info(client: Redis) -> dict:
    """
    Obtiene información del servidor Redis
    """
    try:
        info = client.info()
        return {
            "redis_version": info.get("redis_version"),
            "used_memory_human": info.get("used_memory_human"),
            "connected_clients": info.get("connected_clients"),
            "uptime_in_seconds": info.get("uptime_in_seconds"),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "connection_config": {
                "host": redis_config.host,
                "port": redis_config.port,
                "db": redis_config.db,
                "max_connections": redis_config.max_connections
            }
        }
    except Exception as e:
        logger.error(f"Error al obtener información de Redis: {e}")
        return {}
