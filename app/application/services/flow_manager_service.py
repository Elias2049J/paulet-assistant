# Servicio que gestiona el estado del flujo conversacional para un solo usuario.
# Permite avanzar en el árbol de decisiones y volver al menú principal.
from app.application.interfaces.flow_manager_interface import FlowManagerInterface


class FlowManagerService(FlowManagerInterface):
    def __init__(self, decision_tree):
        self.tree = decision_tree
        self.estado_actual = self.tree.get_root()  # Estado único para un solo usuario

    def avanzar(self, mensaje: str):
        # Avanza el flujo según el mensaje recibido (solo un usuario).
        opciones = self.estado_actual.get_opciones()
        entrada = mensaje.strip()
        siguiente = opciones.get(entrada)
        if siguiente:
            self.estado_actual = siguiente
        # Permite volver al menú principal con palabras clave.
        elif entrada.lower() in ["volver", "inicio", "root"]:
            self.estado_actual = self.tree.get_root()
        return self.estado_actual
