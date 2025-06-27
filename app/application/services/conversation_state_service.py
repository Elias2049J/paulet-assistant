from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ConversationStateService:
    def __init__(self):
        self._estados_usuario: Dict[str, Dict[str, Any]] = {}

    def inicializar_usuario(self, usuario_id: str) -> None:
        """Inicializa el estado para un usuario si no existe"""
        if usuario_id not in self._estados_usuario:
            self._estados_usuario[usuario_id] = {
                "datos_dinamicos": {},
                "menu_actual": "main"
            }
            logger.info(f"Estado inicializado para usuario: {usuario_id}")

    def almacenar_datos_dinamicos(self, usuario_id: str, clave: str, datos: Any) -> None:
        """Almacena datos dinámicos para el usuario"""
        self.inicializar_usuario(usuario_id)
        self._estados_usuario[usuario_id]["datos_dinamicos"][clave] = datos
        logger.info(f"Datos dinámicos almacenados - Usuario: {usuario_id}, Clave: {clave}")

    def obtener_datos_dinamicos(self, usuario_id: str, clave: str) -> Optional[Any]:
        """Obtiene datos dinámicos del usuario"""
        self.inicializar_usuario(usuario_id)
        datos = self._estados_usuario[usuario_id]["datos_dinamicos"].get(clave)
        if datos:
            logger.debug(f"Datos dinámicos recuperados - Usuario: {usuario_id}, Clave: {clave}")
        return datos

    def establecer_menu_actual(self, usuario_id: str, menu_id: str) -> None:
        """Establece el menú actual del usuario"""
        self.inicializar_usuario(usuario_id)
        self._estados_usuario[usuario_id]["menu_actual"] = menu_id
        logger.debug(f"Menú establecido - Usuario: {usuario_id}, Menú: {menu_id}")

    def obtener_menu_actual(self, usuario_id: str) -> str:
        """Obtiene el menú actual del usuario"""
        self.inicializar_usuario(usuario_id)
        return self._estados_usuario[usuario_id]["menu_actual"]

    def limpiar_estado(self, usuario_id: str) -> None:
        """Limpia todo el estado del usuario"""
        if usuario_id in self._estados_usuario:
            del self._estados_usuario[usuario_id]
            logger.info(f"Estado limpiado para usuario: {usuario_id}")

    def limpiar_datos_dinamicos(self, usuario_id: str, clave: Optional[str] = None) -> None:
        """Limpia datos dinámicos específicos o todos"""
        self.inicializar_usuario(usuario_id)
        if clave:
            self._estados_usuario[usuario_id]["datos_dinamicos"].pop(clave, None)
            logger.info(f"Datos dinámicos limpiados - Usuario: {usuario_id}, Clave: {clave}")
        else:
            self._estados_usuario[usuario_id]["datos_dinamicos"].clear()
            logger.info(f"Todos los datos dinámicos limpiados - Usuario: {usuario_id}")