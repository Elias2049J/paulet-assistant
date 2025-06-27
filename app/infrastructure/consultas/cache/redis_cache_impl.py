# Implementación mejorada de la caché usando Redis.
# Permite almacenar y recuperar datos en Redis para cada usuario y ciclo con manejo de errores.
from app.infrastructure.consultas.cache.base_cache_impl import BaseCacheImpl
from app.infrastructure.config.redis_client import redis_client
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RedisCacheImpl(BaseCacheImpl):
    def __init__(self, client: redis_client):
        self.redis_client = client
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0
        }

    def get(self, usuario: str, ciclo: str) -> str:
        """Recupera el valor desde Redis usando la clave construida con manejo de errores."""
        try:
            key = self._build_key(usuario, ciclo)
            raw_data = self.redis_client.get(key)

            if raw_data is not None:
                self._cache_stats["hits"] += 1
                logger.info(f"Cache HIT para clave: {key}")

                try:
                    # Intentar deserializar como JSON con metadata
                    cache_data = json.loads(raw_data)
                    if isinstance(cache_data, dict) and "value" in cache_data:
                        return cache_data["value"]
                    else:
                        # Es un valor directo en JSON
                        return raw_data
                except json.JSONDecodeError:
                    # Es un valor legacy sin JSON, devolverlo directamente
                    return raw_data
            else:
                self._cache_stats["misses"] += 1
                logger.info(f"Cache MISS para clave: {key}")
                return ""

        except Exception as e:
            self._cache_stats["errors"] += 1
            logger.error(f"Error al obtener de caché: {e}")
            return ""

    def set(self, usuario: str, ciclo: str, value: str, ttl: int):
        """Almacena el valor en Redis con TTL y manejo de errores."""
        try:
            key = self._build_key(usuario, ciclo)

            # Crear metadata para el valor
            cache_data = {
                "value": value,
                "timestamp": datetime.now().isoformat(),
                "ttl": ttl,
                "usuario": usuario,
                "ciclo": ciclo
            }

            # Guardar como JSON para incluir metadata
            serialized_data = json.dumps(cache_data)
            self.redis_client.set(key, serialized_data, ex=ttl)

            logger.info(f"Valor guardado en caché con clave: {key}, TTL: {ttl}s")

        except Exception as e:
            self._cache_stats["errors"] += 1
            logger.error(f"Error al guardar en caché: {e}")

    def delete(self, usuario: str, ciclo: str) -> bool:
        """Elimina una entrada específica del caché."""
        try:
            key = self._build_key(usuario, ciclo)
            result = self.redis_client.delete(key)

            if result:
                logger.info(f"Entrada eliminada del caché: {key}")
                return True
            else:
                logger.warning(f"No se encontró entrada para eliminar: {key}")
                return False

        except Exception as e:
            self._cache_stats["errors"] += 1
            logger.error(f"Error al eliminar de caché: {e}")
            return False

    def exists(self, usuario: str, ciclo: str) -> bool:
        """Verifica si una clave existe en el caché."""
        try:
            key = self._build_key(usuario, ciclo)
            return bool(self.redis_client.exists(key))
        except Exception as e:
            logger.error(f"Error al verificar existencia en caché: {e}")
            return False

    def get_ttl(self, usuario: str, ciclo: str) -> int:
        """Obtiene el tiempo de vida restante de una clave en segundos."""
        try:
            key = self._build_key(usuario, ciclo)
            ttl = self.redis_client.ttl(key)
            return ttl if ttl > 0 else 0
        except Exception as e:
            logger.error(f"Error al obtener TTL: {e}")
            return 0

    def extend_ttl(self, usuario: str, ciclo: str, additional_seconds: int) -> bool:
        """Extiende el TTL de una entrada existente."""
        try:
            key = self._build_key(usuario, ciclo)
            current_ttl = self.redis_client.ttl(key)

            if current_ttl > 0:
                new_ttl = current_ttl + additional_seconds
                self.redis_client.expire(key, new_ttl)
                logger.info(f"TTL extendido para {key}: {new_ttl}s")
                return True
            else:
                logger.warning(f"No se puede extender TTL para clave inexistente: {key}")
                return False

        except Exception as e:
            logger.error(f"Error al extender TTL: {e}")
            return False

    def clear_user_cache(self, usuario: str) -> int:
        """Limpia todas las entradas de caché de un usuario específico."""
        try:
            pattern = f"{self.__class__.__name__.lower()}:{usuario}:*"
            keys = self.redis_client.keys(pattern)

            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Eliminadas {deleted} entradas de caché para usuario: {usuario}")
                return deleted
            else:
                logger.info(f"No hay entradas de caché para usuario: {usuario}")
                return 0

        except Exception as e:
            logger.error(f"Error al limpiar caché del usuario: {e}")
            return 0

    def clear_all_cache(self) -> int:
        """Limpia todas las entradas de caché de esta implementación."""
        try:
            pattern = f"{self.__class__.__name__.lower()}:*"
            keys = self.redis_client.keys(pattern)

            if keys:
                deleted = self.redis_client.delete(*keys)
                logger.info(f"Eliminadas {deleted} entradas de caché total")
                return deleted
            else:
                logger.info("No hay entradas de caché para limpiar")
                return 0

        except Exception as e:
            logger.error(f"Error al limpiar todo el caché: {e}")
            return 0

    def get_cache_info(self, usuario: str, ciclo: str) -> Optional[Dict[str, Any]]:
        """Obtiene información detallada sobre una entrada de caché."""
        try:
            key = self._build_key(usuario, ciclo)
            raw_data = self.redis_client.get(key)

            if raw_data:
                try:
                    cache_data = json.loads(raw_data)
                    cache_data["remaining_ttl"] = self.get_ttl(usuario, ciclo)
                    cache_data["key"] = key
                    return cache_data
                except json.JSONDecodeError:
                    # Si no es JSON, es un valor legacy
                    return {
                        "value": raw_data,
                        "key": key,
                        "remaining_ttl": self.get_ttl(usuario, ciclo),
                        "is_legacy": True
                    }
            else:
                return None

        except Exception as e:
            logger.error(f"Error al obtener info de caché: {e}")
            return None

    def get_cache_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de uso del caché."""
        total_operations = sum(self._cache_stats.values())
        hit_rate = (self._cache_stats["hits"] / total_operations * 100) if total_operations > 0 else 0

        return {
            **self._cache_stats,
            "total_operations": total_operations,
            "hit_rate_percent": round(hit_rate, 2)
        }

    def reset_cache_stats(self):
        """Reinicia las estadísticas del caché."""
        self._cache_stats = {
            "hits": 0,
            "misses": 0,
            "errors": 0
        }
        logger.info("Estadísticas de caché reiniciadas")

    def health_check(self) -> Dict[str, Any]:
        """Verifica el estado de salud de la conexión Redis."""
        try:
            # Hacer ping a Redis
            ping_result = self.redis_client.ping()

            # Obtener información del servidor
            redis_info = self.redis_client.info()

            return {
                "status": "healthy" if ping_result else "unhealthy",
                "ping": ping_result,
                "redis_version": redis_info.get("redis_version"),
                "used_memory": redis_info.get("used_memory_human"),
                "connected_clients": redis_info.get("connected_clients"),
                "uptime_in_seconds": redis_info.get("uptime_in_seconds")
            }

        except Exception as e:
            logger.error(f"Error en health check: {e}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
