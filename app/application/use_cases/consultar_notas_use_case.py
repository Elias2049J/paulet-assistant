from app.application.use_cases.base_consultar import ConsultaUseCase
import json
import logging
from app.domain.entities.calificaciones.mappers import crear_calificaciones_por_periodo
from app.infrastructure.presenters.calificacion_presenter import CalificacionPresenter

logger = logging.getLogger(__name__)


class ConsultarNotasUseCase(ConsultaUseCase):
    async def ejecutar_consulta(self):
        """Ejecuta la consulta completa obteniendo períodos y calificaciones"""
        logger.info("Iniciando consulta de notas completa")

        # Primero intenta obtener de caché
        datos = self.obtener_de_cache()
        desde_cache = False

        if datos:
            logger.info("Datos encontrados en caché, deserializando")
            try:
                # Deserializa los datos completos del caché
                datos_completos = json.loads(datos)

                # Reconstruir objetos de dominio para las calificaciones
                periodos_calificaciones = {}
                for periodo, data in datos_completos.get("calificaciones", {}).items():
                    if isinstance(data, dict) and "calificaciones" in data:
                        periodos_calificaciones[periodo] = crear_calificaciones_por_periodo(periodo, data["calificaciones"])
                    else:
                        # Formato legacy - intentar convertir
                        periodos_calificaciones[periodo] = crear_calificaciones_por_periodo(periodo, data)

                # Devolver datos completos
                resultado = {
                    "periodos": datos_completos.get("periodos", []),
                    "calificaciones": periodos_calificaciones
                }
                desde_cache = True
                logger.info(f"Datos cargados desde caché: {len(resultado['periodos'])} períodos")

                # Usar el presentador para formatear la respuesta
                return CalificacionPresenter.formatear_respuesta(
                    resultado["calificaciones"], desde_cache
                )

            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Error deserializando caché, haciendo scraping: {e}")
                # Continuar con scraping si falla la deserialización

        # No hay datos válidos en caché, hacer scraping
        logger.info("Iniciando scraping para obtener datos")
        datos_scraping = await self.obtener_de_fuente(timeout=90)

        if not datos_scraping:
            logger.error("Error o timeout en scraping")
            return "Error obteniendo datos. Por favor intenta nuevamente."

        # Serializar para guardar en caché
        try:
            datos_para_cache = {
                "periodos": datos_scraping.get("periodos", []),
                "calificaciones": {}
            }

            # Serializar las calificaciones
            for periodo, obj_periodo in datos_scraping.get("calificaciones", {}).items():
                datos_para_cache["calificaciones"][periodo] = {
                    "periodo": obj_periodo.periodo,
                    "calificaciones": [cal.to_dict() for cal in obj_periodo.calificaciones]
                }

            # Guardar en caché
            logger.info("Guardando datos en caché")
            self.guardar_en_cache(datos_para_cache)

            # Usar el presentador para formatear la respuesta
            return CalificacionPresenter.formatear_respuesta(
                datos_scraping["calificaciones"],
                False
            )

        except Exception as e:
            logger.error(f"Error procesando resultados de scraping: {e}")
            return "Error procesando resultados. Por favor intenta nuevamente."

    async def obtener_solo_periodos(self, forzar_scraping=False):
        """Método para obtener solo la lista de períodos con timeout"""
        logger.info(f"Obteniendo solo períodos (forzar_scraping: {forzar_scraping})")

        # Si se fuerza el scraping (primera consulta de la sesión), ignorar la caché
        if forzar_scraping:
            logger.info("Se ha solicitado forzar scraping, ignorando caché")
            # Si no hay caché válida o está incompleta, hacer scraping
            logger.info("Realizando scraping para obtener TODOS los datos (períodos y calificaciones)")
            datos_scraping = await self.obtener_de_fuente(timeout=90)

            if datos_scraping and "periodos" in datos_scraping:
                periodos = datos_scraping.get("periodos", [])
                logger.info(f"Períodos obtenidos del scraping: {periodos}")

                # Guardar en caché los datos completos (períodos Y calificaciones)
                if periodos and len(periodos) > 0:
                    try:
                        # Obtener las calificaciones directamente del resultado del scraping
                        calificaciones = datos_scraping.get("calificaciones", {})

                        # Preparar datos completos para la caché
                        datos_para_cache = {
                            "periodos": periodos,
                            "calificaciones": {}
                        }

                        # Verificar que las calificaciones no estén vacías
                        for periodo, obj_periodo in calificaciones.items():
                            cursos_con_datos = []
                            for cal in obj_periodo.calificaciones:
                                # Verificar que la serialización incluya todos los campos
                                cal_dict = cal.to_dict()
                                logger.info(f"Calificación para guardar en caché: {cal_dict}")
                                cursos_con_datos.append(cal_dict)

                            datos_para_cache["calificaciones"][periodo] = {
                                "periodo": obj_periodo.periodo,
                                "calificaciones": cursos_con_datos
                            }

                        # Guardar en caché datos completos
                        logger.info(f"Guardando datos completos en caché: {len(periodos)} períodos con todas sus calificaciones")
                        self.guardar_en_cache(datos_para_cache)
                    except Exception as e:
                        logger.error(f"Error guardando datos completos en caché: {e}")

                return periodos
            else:
                logger.error("Error obteniendo períodos del scraping")
                return []

        # Si no se fuerza scraping, intentar obtener de caché primero
        datos = self.obtener_de_cache()

        if datos:
            logger.info("Datos encontrados en caché, intentando obtener períodos")
            try:
                datos_completos = json.loads(datos)
                periodos = datos_completos.get("periodos", [])
                logger.info(f"Períodos desde caché: {periodos}")

                # Verificar que además de los períodos, las calificaciones también estén en caché
                calificaciones = datos_completos.get("calificaciones", {})
                if periodos and calificaciones and len(periodos) > 0:
                    logger.info(f"Usando datos de caché: {len(periodos)} períodos y {len(calificaciones)} períodos con calificaciones")
                    return periodos
                else:
                    logger.warning("Caché incompleta, realizando scraping")
            except json.JSONDecodeError:
                logger.warning("Error deserializando períodos del caché")
        else:
            logger.info("No hay datos en caché, realizando scraping")

        # Si no hay caché válida o está incompleta, hacer scraping
        logger.info("Realizando scraping para obtener TODOS los datos (períodos y calificaciones)")
        datos_scraping = await self.obtener_de_fuente(timeout=90)

        if datos_scraping and "periodos" in datos_scraping:
            periodos = datos_scraping.get("periodos", [])
            logger.info(f"Períodos obtenidos del scraping: {periodos}")

            # Guardar en caché los datos completos (períodos Y calificaciones)
            if periodos and len(periodos) > 0:
                try:
                    # Obtener las calificaciones directamente del resultado del scraping
                    calificaciones = datos_scraping.get("calificaciones", {})

                    # Preparar datos completos para la caché
                    datos_para_cache = {
                        "periodos": periodos,
                        "calificaciones": {}
                    }

                    # Verificar que las calificaciones no estén vacías
                    for periodo, obj_periodo in calificaciones.items():
                        cursos_con_datos = []
                        for cal in obj_periodo.calificaciones:
                            # Verificar que la serialización incluya todos los campos
                            cal_dict = cal.to_dict()
                            logger.info(f"Calificación para guardar en caché: {cal_dict}")
                            cursos_con_datos.append(cal_dict)

                        datos_para_cache["calificaciones"][periodo] = {
                            "periodo": obj_periodo.periodo,
                            "calificaciones": cursos_con_datos
                        }

                    # Guardar en caché datos completos
                    logger.info(f"Guardando datos completos en caché: {len(periodos)} períodos con todas sus calificaciones")
                    self.guardar_en_cache(datos_para_cache)
                except Exception as e:
                    logger.error(f"Error guardando datos completos en caché: {e}")

            return periodos

        # Si el scraping falló, intentar recuperar datos de caché como respaldo
        logger.warning("Scraping falló, intentando recuperar desde caché como respaldo")
        if datos:
            try:
                datos_completos = json.loads(datos)
                periodos = datos_completos.get("periodos", [])
                logger.info(f"Períodos desde caché (respaldo): {periodos}")

                if periodos and len(periodos) > 0:
                    return periodos
            except json.JSONDecodeError:
                logger.warning("Error deserializando períodos del caché")

        logger.error("Error obteniendo períodos - ni scraping ni caché funcionaron")
        return []

    async def obtener_calificaciones_periodo(self, periodo_seleccionado):
        """Método para obtener calificaciones de un período específico"""
        logger.info(f"Obteniendo calificaciones para período: {periodo_seleccionado}")

        # Intentar obtener siempre de caché primero, ya que los datos completos deberían estar allí
        datos = self.obtener_de_cache()

        if datos:
            logger.info("Datos encontrados en caché")
            try:
                datos_completos = json.loads(datos)
                calificaciones_data = datos_completos.get("calificaciones", {})

                if periodo_seleccionado in calificaciones_data:
                    periodo_data = calificaciones_data[periodo_seleccionado]
                    logger.info(f"Encontradas calificaciones para período {periodo_seleccionado} en caché")

                    if isinstance(periodo_data, dict) and "calificaciones" in periodo_data:
                        return crear_calificaciones_por_periodo(periodo_seleccionado, periodo_data["calificaciones"])
                    else:
                        return crear_calificaciones_por_periodo(periodo_seleccionado, periodo_data)
                else:
                    logger.warning(f"Período {periodo_seleccionado} no encontrado en caché")
            except json.JSONDecodeError as e:
                logger.warning(f"Error deserializando datos de caché: {e}")

        # Si no se encontró en caché o hubo error, intentar hacer scraping
        logger.info(f"No se encontraron datos en caché para período {periodo_seleccionado}, haciendo scraping")
        datos_scraping = await self.obtener_de_fuente(timeout=90)

        if datos_scraping and "calificaciones" in datos_scraping:
            # Guardar los datos completos en caché para futuras consultas
            try:
                datos_para_cache = {
                    "periodos": datos_scraping.get("periodos", []),
                    "calificaciones": {}
                }

                # Serializar todas las calificaciones
                for periodo, obj_periodo in datos_scraping.get("calificaciones", {}).items():
                    datos_para_cache["calificaciones"][periodo] = {
                        "periodo": obj_periodo.periodo,
                        "calificaciones": [cal.to_dict() for cal in obj_periodo.calificaciones]
                    }

                # Guardar en caché
                logger.info("Guardando datos completos en caché después de scraping de respaldo")
                self.guardar_en_cache(datos_para_cache)
            except Exception as e:
                logger.error(f"Error guardando datos en caché: {e}")

            # Devolver solo las calificaciones del período solicitado
            calificaciones = datos_scraping.get("calificaciones", {})
            return calificaciones.get(periodo_seleccionado)

        logger.error(f"Error obteniendo calificaciones para período {periodo_seleccionado}")
        return None
