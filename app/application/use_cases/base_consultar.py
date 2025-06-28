from abc import ABC, abstractmethod
import asyncio
import inspect
import logging
import json
from typing import Any, Optional

logger = logging.getLogger(__name__)


class ConsultaUseCase(ABC):
    """Clase base para casos de uso de consulta"""

    def __init__(self, extractor, cache, usuario):
        self.extractor = extractor  # Instancia del extractor de datos
        self.cache = cache          # Instancia de la caché
        self.usuario = usuario      # Usuario actual
        self.cache_key = f"{self.__class__.__name__}:{usuario}"

    def obtener_de_cache(self, clave_adicional: str = None) -> Optional[str]:
        """Obtiene resultado desde caché con manejo de errores"""
        try:
            clave = self.cache_key
            if clave_adicional:
                clave = f"{clave}:{clave_adicional}"

            logger.debug(f"Intentando obtener datos de caché con clave: {clave}")
            datos = self.cache.get(self.usuario)

            if datos:
                logger.info(f"Datos encontrados en caché para {clave}")
                return datos
            logger.info(f"No se encontraron datos en caché para {clave}")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo datos de caché: {e}")
            return None

    async def obtener_de_fuente(self, timeout: int = 60) -> Any:
        """Obtiene el resultado desde la fuente (scraping) con timeout"""
        try:
            logger.info(f"Obteniendo datos de fuente con timeout de {timeout}s")
            metodo_extraer = self.extractor.scrap

            if inspect.iscoroutinefunction(metodo_extraer):
                return await asyncio.wait_for(metodo_extraer(), timeout=timeout)
            return metodo_extraer()
        except asyncio.TimeoutError:
            logger.error(f"Timeout de {timeout}s excedido al obtener datos de fuente")
            return None
        except Exception as e:
            logger.error(f"Error obteniendo datos de fuente: {e}")
            return None

    def guardar_en_cache(self, resultado: Any, ttl: int = 3600, clave_adicional: str = None) -> bool:
        """Guarda el resultado en caché con TTL"""
        try:
            if not resultado:
                logger.warning("No se guardaron datos en caché: resultado vacío")
                return False

            clave = self.cache_key
            if clave_adicional:
                clave = f"{clave}:{clave_adicional}"

            # Convertir a string si es necesario
            datos_cache = resultado
            if not isinstance(resultado, str):
                datos_cache = json.dumps(resultado)

            logger.info(f"Guardando datos en caché con clave: {clave}, TTL: {ttl}s")
            self.cache.set(self.usuario, datos_cache, ttl)
            return True
        except Exception as e:
            logger.error(f"Error guardando datos en caché: {e}")
            return False

    @abstractmethod
    async def ejecutar_consulta(self) -> Any:
        """Debe ser implementado por los casos de uso concretos"""
        pass
