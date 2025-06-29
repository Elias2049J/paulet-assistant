import logging
from typing import Dict, Any, Optional, List, Tuple
from app.application.services.conversation_state_service import ConversationStateService
from app.application.services.menu_service import MenuService
from app.domain.entities.menu.menu_item import MenuItem, MenuOption

logger = logging.getLogger(__name__)


class ChatbotService:
    def __init__(self, menus: Dict[str, MenuItem], use_cases: Dict[str, Any]):
        self.menus = menus
        self.use_cases = use_cases
        self.state_service = ConversationStateService()
        self.menu_service = MenuService(menus, self.state_service)
        self._usuarios_iniciados = set()
        self._sesiones_con_scraping_realizado = set()  # Controla si ya se hizo scraping en esta sesión

    async def procesar_consulta(self, mensaje: str, usuario_id: str = "default") -> str:
        """Procesa una consulta del usuario"""
        try:
            # Inicializar estado del usuario
            self.state_service.inicializar_usuario(usuario_id)

            # Si es el primer mensaje, mostrar menú principal
            if usuario_id not in self._usuarios_iniciados:
                self._usuarios_iniciados.add(usuario_id)
                return self.menu_service.get_initial_menu(usuario_id)

            # Obtener menú actual
            menu_actual_id = self.state_service.obtener_menu_actual(usuario_id)
            menu_actual = self.menus.get(menu_actual_id)

            if not menu_actual:
                logger.error(f"Menú no encontrado: {menu_actual_id}")
                return "Error: menú no encontrado. Iniciando de nuevo."

            # Verificar si está en pantalla de resultados de notas
            if menu_actual_id == "seleccionar_periodo" and self.state_service.obtener_datos_dinamicos(usuario_id, "mostrando_resultados"):
                # Estamos mostrando resultados de notas, manejar opciones de navegación post-resultados
                return await self._manejar_navegacion_post_resultados(mensaje, usuario_id)

            # Verificar si está en pantalla de resultados de horarios
            if self.state_service.obtener_datos_dinamicos(usuario_id, "mostrando_horarios"):
                # Estamos mostrando resultados de horarios, manejar opciones de navegación
                return await self._manejar_navegacion_post_horarios(mensaje, usuario_id)

            # Usar MenuService para procesar la entrada del usuario
            respuesta, accion = self.menu_service.process_user_input(mensaje, usuario_id)

            # Si hay una acción que ejecutar
            if accion:
                resultado_accion = await self._ejecutar_accion(accion, usuario_id)

                # Manejar navegación post-acción
                if accion == "obtener_periodos_notas":
                    return self.menu_service.navigate_to_menu("seleccionar_periodo", usuario_id)
                elif accion == "consultar_notas_periodo":
                    # El presentador ya incluye las opciones de navegación
                    return resultado_accion
                elif accion == "consultar_horarios":
                    # Marcar que estamos mostrando horarios para manejar navegación posterior
                    self.state_service.almacenar_datos_dinamicos(usuario_id, "mostrando_horarios", True)
                    # El presentador ya incluye las opciones de navegación
                    return resultado_accion
                else:
                    return resultado_accion

            return respuesta

        except Exception as e:
            logger.error(f"Error procesando consulta: {e}")
            return "Lo siento, ocurrió un error al procesar tu solicitud. Por favor intenta nuevamente."

    async def _manejar_navegacion_post_resultados(self, mensaje: str, usuario_id: str) -> str:
        """Maneja las opciones después de mostrar resultados de notas"""
        try:
            opcion = int(mensaje)

            if opcion == 1:
                # Seleccionar otro período - volver al menú de selección de período
                logger.info(f"Usuario {usuario_id} seleccionó ver otro período")
                self.state_service.almacenar_datos_dinamicos(usuario_id, "mostrando_resultados", False)
                return self.menu_service.navigate_to_menu("seleccionar_periodo", usuario_id)
            elif opcion == 2:
                # Volver al menú principal
                logger.info(f"Usuario {usuario_id} seleccionó volver al menú principal")
                self.state_service.almacenar_datos_dinamicos(usuario_id, "mostrando_resultados", False)
                self.state_service.establecer_menu_actual(usuario_id, "main")
                return self.menu_service.navigate_to_menu("main", usuario_id)
            else:
                return "Opción no válida. Por favor selecciona 1 para ver otro período o 2 para volver al menú principal."

        except ValueError:
            return "Por favor ingresa un número válido (1 o 2)."
        except Exception as e:
            logger.error(f"Error en navegación post-resultados: {e}")
            return "Error procesando la selección. Intenta nuevamente."

    async def _manejar_navegacion_post_horarios(self, mensaje: str, usuario_id: str) -> str:
        """Maneja las opciones después de mostrar resultados de horarios"""
        try:
            opcion = int(mensaje)

            if opcion == 1:
                # Volver al menú principal
                logger.info(f"Usuario {usuario_id} seleccionó volver al menú principal desde horarios")
                # Limpiar estado de horarios
                self.state_service.almacenar_datos_dinamicos(usuario_id, "mostrando_horarios", False)
                self.state_service.establecer_menu_actual(usuario_id, "main")
                return self.menu_service.navigate_to_menu("main", usuario_id)
            else:
                return "Opción no válida. Por favor selecciona 1 para volver al menú principal."

        except ValueError:
            return "Por favor ingresa un número válido."
        except Exception as e:
            logger.error(f"Error en navegación post-horarios: {e}")
            return "Error procesando la selección. Intenta nuevamente."

    # Centraliza la logica de ejecucion de acciones
    async def _ejecutar_accion(self, accion: str, usuario_id: str) -> str:
        """Ejecuta una acción específica"""
        logger.info(f"Ejecutando acción: {accion} para usuario: {usuario_id}")

        if accion == "obtener_periodos_notas":
            return await self._obtener_periodos_notas(usuario_id)
        elif accion == "consultar_notas_periodo":
            return await self._consultar_notas_periodo(usuario_id)
        elif accion == "consultar_horarios":
            return await self._consultar_horarios(usuario_id)
        else:
            logger.warning(f"Acción no reconocida: {accion}")
            return "Acción no disponible en este momento."

    async def _obtener_periodos_notas(self, usuario_id: str) -> str:
        """Obtiene los períodos disponibles para consultar notas"""
        try:
            logger.info(f"[CONSULTA NOTAS] Iniciando obtención de períodos para usuario: {usuario_id}")
            use_case = self.use_cases.get("consultar_notas")
            if not use_case:
                logger.error("[CONSULTA NOTAS] Caso de uso consultar_notas no disponible")
                return "Error: Servicio de consulta de notas no disponible temporalmente."

            # Verificar si es la primera vez que se consulta notas en esta sesión
            primer_consulta_sesion = f"{usuario_id}_notas" not in self._sesiones_con_scraping_realizado
            logger.info(f"[CONSULTA NOTAS] ¿Primera consulta de notas en la sesión? {primer_consulta_sesion}")

            # Verificar si ya tenemos períodos almacenados en el estado del usuario
            periodos_almacenados = self.state_service.obtener_datos_dinamicos(usuario_id, "periodos_obtenidos")
            if not primer_consulta_sesion and periodos_almacenados:
                logger.info(f"[CONSULTA NOTAS] Usando períodos ya almacenados en estado: {periodos_almacenados}")
                return self.menu_service.navigate_to_menu("seleccionar_periodo", usuario_id)

            # Pasar el indicador de forzar scraping al caso de uso
            logger.info("[CONSULTA NOTAS] Ejecutando obtener_solo_periodos()")
            periodos = await use_case.obtener_solo_periodos(forzar_scraping=primer_consulta_sesion)

            # Marcar que ya se realizó scraping para esta sesión
            if primer_consulta_sesion:
                self._sesiones_con_scraping_realizado.add(f"{usuario_id}_notas")
                logger.info(f"[CONSULTA NOTAS] Marcando que scraping ha sido realizado para sesión de {usuario_id}")

            logger.info(f"[CONSULTA NOTAS] Períodos obtenidos: {periodos}")

            if not periodos:
                logger.warning("[CONSULTA NOTAS] No se encontraron períodos disponibles")
                return "No se encontraron períodos disponibles. Por favor intenta más tarde."

            # Almacenar períodos en el estado del usuario
            self.state_service.almacenar_datos_dinamicos(usuario_id, "periodos_obtenidos", periodos)
            logger.info(f"[CONSULTA NOTAS] {len(periodos)} períodos almacenados en estado para usuario: {usuario_id}")

            # Retornar directamente el menú de selección de período
            return self.menu_service.navigate_to_menu("seleccionar_periodo", usuario_id)

        except Exception as e:
            logger.error(f"[CONSULTA NOTAS] Error obteniendo períodos: {e}", exc_info=True)
            return "Error al obtener los períodos académicos. Por favor intenta nuevamente más tarde."

    async def _consultar_notas_periodo(self, usuario_id: str) -> str:
        """Consulta notas de un período específico"""
        try:
            logger.info(f"[CONSULTA NOTAS] Iniciando consulta de notas para usuario: {usuario_id}")
            periodo_seleccionado = self.state_service.obtener_datos_dinamicos(usuario_id, "seleccion_actual")
            if not periodo_seleccionado:
                logger.warning(f"[CONSULTA NOTAS] No se encontró período seleccionado para usuario: {usuario_id}")
                return "Error: No se pudo identificar el período seleccionado."

            logger.info(f"[CONSULTA NOTAS] Consultando notas del período: {periodo_seleccionado}")
            use_case_notas = self.use_cases.get("consultar_notas")
            if not use_case_notas:
                logger.error("[CONSULTA NOTAS] Caso de uso consultar_notas no disponible")
                return "Error: Servicio de consulta de notas no disponible temporalmente."

            periodo_obj = await use_case_notas.obtener_calificaciones_periodo(periodo_seleccionado)
            logger.info(f"[CONSULTA NOTAS] Calificaciones obtenidas para período {periodo_seleccionado}")

            if periodo_obj:
                # Log detallado para depuración
                logger.info(f"[CONSULTA NOTAS] Objeto período: {periodo_obj}")
                for idx, cal in enumerate(periodo_obj.calificaciones):
                    logger.info(f"[CONSULTA NOTAS] Calificación {idx+1}: {cal.curso} - PF: {cal.pf} - Faltas: {cal.faltas}/{cal.max_faltas}")

                # Usar el presentador para formatear la respuesta con opciones de navegación
                from app.infrastructure.presenters.calificacion_presenter import CalificacionPresenter
                respuesta = CalificacionPresenter.formatear_respuesta_periodo(periodo_obj, periodo_seleccionado)

                # Marcar que estamos mostrando resultados
                self.state_service.almacenar_datos_dinamicos(usuario_id, "mostrando_resultados", True)
                logger.info(f"[CONSULTA NOTAS] Mostrando {len(periodo_obj.calificaciones)} calificaciones al usuario")
                return respuesta
            else:
                logger.warning(f"[CONSULTA NOTAS] No se encontraron calificaciones para el período {periodo_seleccionado}")
                return f"No se encontraron notas para el período {periodo_seleccionado}."

        except Exception as e:
            logger.error(f"[CONSULTA NOTAS] Error consultando notas del período: {e}", exc_info=True)
            return "Error al consultar las notas. Por favor intenta nuevamente más tarde."

    async def _consultar_horarios(self, usuario_id: str) -> str:
        """Consulta los horarios del usuario"""
        try:
            logger.info(f"[CONSULTA HORARIOS] Iniciando consulta de horarios para usuario: {usuario_id}")
            use_case = self.use_cases.get("consultar_horarios")
            if not use_case:
                logger.error("[CONSULTA HORARIOS] Caso de uso consultar_horarios no disponible")
                return "Error: Servicio de consulta de horarios no disponible temporalmente."

            logger.info("[CONSULTA HORARIOS] Ejecutando caso de uso")
            resultado = await use_case.ejecutar_consulta()
            logger.info("[CONSULTA HORARIOS] Consulta completada exitosamente")
            return resultado

        except Exception as e:
            logger.error(f"[CONSULTA HORARIOS] Error consultando horarios: {e}", exc_info=True)
            return "Error al consultar los horarios. Por favor intenta nuevamente más tarde."
