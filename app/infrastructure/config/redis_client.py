# Configuración del cliente Redis para la caché de la aplicación.
# Permite la conexión a Redis usando variables de entorno o valores por defecto.
from redis import Redis
import os


def redis_client():
    return Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
        encoding="utf-8",
        decode_responses=True
    )