import logging
from typing import Dict, Optional
from app.domain.entities.menu.menu_item import MenuItem, MenuOption
from app.application.services.conversation_state_service import ConversationStateService

logger = logging.getLogger(__name__)


class MenuService:
    """Servicio simplificado para manejar menús conversacionales"""

    def __init__(self, menus: Dict[str, MenuItem], state_service: ConversationStateService):
        self.menus = menus
        self.state_service = state_service
        self.current_menu_by_user: Dict[str, str] = {}

    def get_initial_menu(self, usuario_id: str = "default") -> str:
        """Obtiene el menú inicial para un usuario"""
        self.current_menu_by_user[usuario_id] = "main"
        return self._render_menu("main", usuario_id)

    def process_user_input(self, message: str, usuario_id: str = "default") -> tuple[str, Optional[str]]:
        """
        Procesa la entrada del usuario y retorna (respuesta, acción_a_ejecutar)
        """
        current_menu_id = self.current_menu_by_user.get(usuario_id, "main")
        current_menu = self.menus.get(current_menu_id)

        if not current_menu:
            return "Error: menú no encontrado", None

        # Si es un menú dinámico, manejar opciones dinámicas
        if current_menu.is_dynamic:
            return self._handle_dynamic_menu(current_menu, message, usuario_id)

        # Buscar la opción seleccionada
        selected_option = self._find_option_by_key(current_menu, message)
        if not selected_option:
            return "Opción no válida. Por favor selecciona una opción correcta.", None

        # Si la opción tiene una acción, ejecutarla
        if selected_option.action:
            return self._handle_action(selected_option.action, usuario_id)

        # Si la opción navega a otro menú
        if selected_option.target_menu_id:
            self.current_menu_by_user[usuario_id] = selected_option.target_menu_id
            return self._render_menu(selected_option.target_menu_id, usuario_id), None

        return "Configuración de menú incompleta", None

    def navigate_to_menu(self, menu_id: str, usuario_id: str = "default") -> str:
        """Navega directamente a un menú específico"""
        self.current_menu_by_user[usuario_id] = menu_id
        return self._render_menu(menu_id, usuario_id)

    def _render_menu(self, menu_id: str, usuario_id: str) -> str:
        """Renderiza un menú para mostrar al usuario"""
        menu = self.menus.get(menu_id)
        if not menu:
            return "Error: menú no encontrado"

        # Si es dinámico, obtener datos y renderizar opciones dinámicas
        if menu.is_dynamic and menu.dynamic_data_key:
            return self._render_dynamic_menu(menu, usuario_id)

        # Renderizar menú estático
        lines = [menu.message]
        for option in menu.options:
            lines.append(f"{option.key}. {option.label}")

        return "\n".join(lines)

    def _render_dynamic_menu(self, menu: MenuItem, usuario_id: str) -> str:
        """Renderiza un menú con opciones dinámicas"""
        lines = [menu.message]

        # Obtener datos dinámicos
        dynamic_data = self.state_service.obtener_datos_dinamicos(usuario_id, menu.dynamic_data_key)
        if not dynamic_data:
            dynamic_data = []

        # Agregar opciones dinámicas
        for i, data_item in enumerate(dynamic_data, 1):
            lines.append(f"{i}. Período {data_item}")

        # Agregar opciones fijas
        for option in menu.options:
            option_number = len(dynamic_data) + int(option.key)
            lines.append(f"{option_number}. {option.label}")

        return "\n".join(lines)

    def _handle_dynamic_menu(self, menu: MenuItem, message: str, usuario_id: str) -> tuple[str, Optional[str]]:
        """Maneja la selección en menús dinámicos"""
        try:
            option_number = int(message)
            dynamic_data = self.state_service.obtener_datos_dinamicos(usuario_id, menu.dynamic_data_key) or []

            logger.info(f"Procesando opción dinámica {option_number} con {len(dynamic_data)} elementos disponibles")

            # Si es una opción dinámica (períodos)
            if 1 <= option_number <= len(dynamic_data):
                selected_data = dynamic_data[option_number - 1]
                self.state_service.almacenar_datos_dinamicos(usuario_id, "seleccion_actual", selected_data)

                logger.info(f"Usuario {usuario_id} seleccionó período: {selected_data}")

                # Si hay una acción definida para el menú dinámico, ejecutarla
                if menu.action:
                    logger.info(f"Ejecutando acción del menú dinámico: {menu.action}")
                    return self._handle_action(menu.action, usuario_id)

                return f"Seleccionaste: Período {selected_data}", None

            # Si es una opción fija (volver al menú principal)
            adjusted_key = str(option_number - len(dynamic_data))
            fixed_option = self._find_option_by_key(menu, adjusted_key)
            if fixed_option:
                logger.info(f"Usuario seleccionó opción fija: {fixed_option.label}")
                if fixed_option.target_menu_id:
                    self.current_menu_by_user[usuario_id] = fixed_option.target_menu_id
                    return self._render_menu(fixed_option.target_menu_id, usuario_id), None

                if fixed_option.action:
                    return self._handle_action(fixed_option.action, usuario_id)

            return "Opción no válida", None

        except ValueError:
            return "Por favor ingresa un número válido", None
        except Exception as e:
            logger.error(f"Error en manejo de menú dinámico: {e}")
            return "Error procesando la selección. Intenta nuevamente.", None

    def _find_option_by_key(self, menu: MenuItem, key: str) -> Optional[MenuOption]:
        """Encuentra una opción por su clave"""
        for option in menu.options:
            if option.key == key:
                return option
        return None

    def _handle_action(self, action: str, usuario_id: str) -> tuple[str, str]:
        """Maneja acciones específicas"""
        # Retorna el mensaje y la acción para que el ChatbotService la ejecute
        return f"Ejecutando acción: {action}", action
