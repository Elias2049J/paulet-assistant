# Configuración del cliente Redis para la caché de la aplicación.
# Permite la conexión a Redis usando variables de entorno o valores por defecto.
import redis
import os

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=0,
    decode_responses=False
)
