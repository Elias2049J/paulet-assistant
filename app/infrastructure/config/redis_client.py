# Configuración del cliente Redis para la caché de la aplicación.
# Permite la conexión a Redis usando variables de entorno o valores por defecto.
import aioredis
import os


async def redis_client():
    return await aioredis.from_url(
        f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', 6379)}",
        encoding="utf-8",
        decode_responses=True
    )
