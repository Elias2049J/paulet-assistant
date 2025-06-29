from app.application.use_cases.base_consultar import ConsultaUseCase
import json
import logging
from app.domain.entities.horarios.mappers import dict_to_horario_diario
from app.infrastructure.presenters.horarios_presenter import HorariosPresenter

logger = logging.getLogger(__name__)


class ConsultarHorariosUseCase(ConsultaUseCase):
    async def ejecutar_consulta(self):
        """Ejecuta la consulta completa de horarios"""
        logger.info("Iniciando consulta de horarios")
        return await self.obtener_horarios()

    async def obtener_horarios(self, forzar_scraping=False):
        """Obtiene los horarios, forzando scraping si se indica"""
        logger.info(f"Obteniendo horarios (forzar_scraping={forzar_scraping})")

        if forzar_scraping:
            logger.info("Forzando scraping de horarios, ignorando caché")
            horarios = await self.obtener_de_fuente(timeout=60)
            if horarios:
                try:
                    datos_para_cache = {}
                    for dia, obj_horario in horarios.items():
                        cursos_validos = [
                            curso for curso in obj_horario.cursos
                            if curso.curso and not curso.curso.isdigit() and curso.curso not in ["Error: formato no válido", "periodos"]
                        ]
                        if cursos_validos:
                            datos_para_cache[dia] = {
                                "dia": obj_horario.dia,
                                "cursos": [curso.to_dict() for curso in cursos_validos],
                            }
                    logger.info(f"Guardando datos en caché: {len(datos_para_cache)} días con clases")
                    self.guardar_en_cache(datos_para_cache)
                    return HorariosPresenter.formatear_respuesta(horarios, False)
                except Exception as e:
                    logger.error(f"Error procesando resultados de scraping: {e}", exc_info=True)
            logger.warning("Scraping falló o no retornó datos, intentando caché como respaldo")
            datos = self.obtener_de_cache()
            if datos:
                logger.info("Datos encontrados en caché, deserializando")
                try:
                    horarios_dict = json.loads(datos)
                    horarios = {}
                    for dia, h in horarios_dict.items():
                        if isinstance(h, dict) and "cursos" in h:
                            cursos_data = h["cursos"]
                            cursos_validos_dia = [
                                c for c in cursos_data
                                if isinstance(c, dict) and
                                   c.get("curso") and
                                   not str(c.get("curso")).isdigit() and
                                   c.get("curso") not in ["Error: formato no válido", "periodos"]
                            ]
                            if cursos_validos_dia:
                                horarios[dia] = dict_to_horario_diario(dia, cursos_validos_dia)
                    return HorariosPresenter.formatear_respuesta(horarios, True)
                except (json.JSONDecodeError, KeyError) as e:
                    logger.warning(f"Error deserializando caché: {e}")
            logger.error("No se pudieron obtener datos ni por scraping ni por caché")
            return "Error obteniendo horarios. Por favor intenta nuevamente."

        # Si no se fuerza scraping, intentar obtener de caché primero
        datos = self.obtener_de_cache()
        if datos:
            logger.info("Datos encontrados en caché, deserializando")
            try:
                horarios_dict = json.loads(datos)
                horarios = {}
                for dia, h in horarios_dict.items():
                    if isinstance(h, dict) and "cursos" in h:
                        cursos_data = h["cursos"]
                        cursos_validos_dia = [
                            c for c in cursos_data
                            if isinstance(c, dict) and
                               c.get("curso") and
                               not str(c.get("curso")).isdigit() and
                               c.get("curso") not in ["Error: formato no válido", "periodos"]
                        ]
                        if cursos_validos_dia:
                            horarios[dia] = dict_to_horario_diario(dia, cursos_validos_dia)
                return HorariosPresenter.formatear_respuesta(horarios, True)
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Error deserializando caché: {e}")
                # Si falla la deserialización, continuar con scraping

        # Si no hay datos en caché, hacer scraping
        logger.info("No hay datos válidos en caché, iniciando scraping para obtener datos frescos")
        horarios = await self.obtener_de_fuente(timeout=60)
        if horarios:
            try:
                datos_para_cache = {}
                for dia, obj_horario in horarios.items():
                    cursos_validos = [
                        curso for curso in obj_horario.cursos
                        if curso.curso and not curso.curso.isdigit() and curso.curso not in ["Error: formato no válido", "periodos"]
                    ]
                    if cursos_validos:
                        datos_para_cache[dia] = {
                            "dia": obj_horario.dia,
                            "cursos": [curso.to_dict() for curso in cursos_validos],
                        }
                logger.info(f"Guardando datos en caché: {len(datos_para_cache)} días con clases")
                self.guardar_en_cache(datos_para_cache)
                return HorariosPresenter.formatear_respuesta(horarios, False)
            except Exception as e:
                logger.error(f"Error procesando resultados de scraping: {e}", exc_info=True)
        logger.error("No se pudieron obtener datos ni por caché ni por scraping")
        return "Error obteniendo horarios. Por favor intenta nuevamente."

