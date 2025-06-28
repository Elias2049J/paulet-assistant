# Rutas para administrar el caché Redis
# Proporciona endpoints para monitorear y gestionar el caché
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class CacheDeleteRequest(BaseModel):
    usuario: str


class CacheStatsResponse(BaseModel):
    hits: int
    misses: int
    errors: int
    total_operations: int
    hit_rate_percent: float


def get_cache_router(cache_impl):
    """Registra las rutas de administración de caché"""

    @router.get("/cache/health")
    def cache_health():
        """Verifica el estado de salud del caché Redis"""
        health_info = cache_impl.health_check()
        if health_info.get("status") == "unhealthy":
            raise HTTPException(status_code=503, detail="Cache is unhealthy")
        return health_info

    @router.get("/cache/stats")
    def cache_stats():
        """Obtiene estadísticas de uso del caché"""
        return cache_impl.get_cache_stats()

    @router.post("/cache/reset-stats")
    def reset_cache_stats():
        """Reinicia las estadísticas del caché"""
        cache_impl.reset_cache_stats()
        return {"message": "Estadísticas reiniciadas"}

    @router.get("/cache/info/{usuario}")
    def cache_info(usuario: str):
        """Obtiene información detallada de una entrada específica"""
        info = cache_impl.get_cache_info(usuario)
        if not info:
            raise HTTPException(status_code=404, detail="Entrada no encontrada en caché")
        return info

    @router.delete("/cache/entry")
    def delete_cache_entry(request: CacheDeleteRequest):
        """Elimina una entrada específica del caché"""
        deleted = cache_impl.delete(request.usuario)
        if not deleted:
            raise HTTPException(status_code=404, detail="Entrada no encontrada")
        return {"message": "Entrada eliminada exitosamente"}

    @router.delete("/cache/user/{usuario}")
    def clear_user_cache(usuario: str):
        """Limpia todas las entradas de caché de un usuario"""
        deleted_count = cache_impl.clear_user_cache(usuario)
        return {
            "message": f"Caché del usuario {usuario} limpiado",
            "deleted_entries": deleted_count
        }

    @router.get("/cache/exists/{usuario}")
    def cache_exists(usuario: str):
        """Verifica si existe una entrada en el caché"""
        exists = cache_impl.exists(usuario)
        ttl = cache_impl.get_ttl(usuario) if exists else 0
        return {
            "exists": exists,
            "ttl_seconds": ttl
        }

    @router.delete("/cache/clear-all")
    def clear_all_cache():
        """Limpia todo el caché de la aplicación"""
        deleted_count = cache_impl.clear_all_cache()
        return {
            "message": "Todo el caché ha sido limpiado",
            "deleted_entries": deleted_count
        }

    @router.get("/cache/keys/{pattern}")
    def get_cache_keys(pattern: str = "*"):
        """Obtiene todas las claves que coinciden con el patrón"""
        try:
            keys = cache_impl.redis_client.keys(pattern)
            return {
                "pattern": pattern,
                "keys": keys,
                "count": len(keys)
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al obtener claves: {str(e)}")

    return router
