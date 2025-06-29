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

        # Primero, intenta siempre hacer scraping al inicio para datos frescos
        logger.info("Iniciando scraping para obtener datos frescos")
        horarios = await self.obtener_de_fuente(timeout=60)
        desde_cache = False

        if horarios:
            # Serializar para guardar en caché
            try:
                datos_para_cache = {}

                # Serializar los horarios (solo datos válidos)
                for dia, obj_horario in horarios.items():
                    # Filtrar solo cursos válidos
                    cursos_validos = [
                        curso for curso in obj_horario.cursos
                        if curso.curso and not curso.curso.isdigit() and curso.curso not in ["Error: formato no válido", "periodos"]
                    ]

                    # Solo guardar días con cursos válidos
                    if cursos_validos:
                        datos_para_cache[dia] = {
                            "dia": obj_horario.dia,
                            "cursos": [curso.to_dict() for curso in cursos_validos],
                        }

                # Guardar en caché
                logger.info(f"Guardando datos en caché: {len(datos_para_cache)} días con clases")
                self.guardar_en_cache(datos_para_cache)

                # Usar el presentador para formatear la respuesta
                return HorariosPresenter.formatear_respuesta(horarios, False)
            except Exception as e:
                logger.error(f"Error procesando resultados de scraping: {e}", exc_info=True)
                # Si falla el guardado, intentar usar la caché como respaldo

        # Si el scraping falla, usar caché como respaldo
        logger.warning("Scraping falló o no retornó datos, intentando caché como respaldo")
        datos = self.obtener_de_cache()

        if datos:
            logger.info("Datos encontrados en caché, deserializando")
            try:
                # Deserializa los datos de caché
                horarios_dict = json.loads(datos)

                # Reconstruir objetos de dominio para los horarios
                horarios = {}
                total_cursos = 0
                cursos_validos = 0

                for dia, h in horarios_dict.items():
                    if isinstance(h, dict) and "cursos" in h:
                        # Filtrar solo cursos válidos
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
                            total_cursos += len(cursos_validos_dia)
                            cursos_validos += len(cursos_validos_dia)

                logger.info(f"Datos en caché: {total_cursos} cursos totales, {cursos_validos} cursos válidos")

                desde_cache = True
                logger.info(f"Datos cargados desde caché: {len(horarios)} días, {cursos_validos} cursos válidos")

                # Usar el presentador para formatear la respuesta
                return HorariosPresenter.formatear_respuesta(horarios, desde_cache)

            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Error deserializando caché: {e}")

        # Si no hay datos ni en scraping ni en caché
        logger.error("No se pudieron obtener datos ni por scraping ni por caché")
        return "Error obteniendo horarios. Por favor intenta nuevamente."

