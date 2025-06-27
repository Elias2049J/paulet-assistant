# Servicio que gestiona el estado del flujo conversacional para un solo usuario.
# Permite avanzar en el árbol de decisiones y volver al menú principal.
from app.application.interfaces.flow_manager_interface import FlowManagerInterface
from app.application.services.decision_tree_service import DecisionTreeService
from app.domain.entities.decision_tree.decision_tree import DecisionTree


class FlowManagerService(FlowManagerInterface):
    def __init__(self, decision_tree: DecisionTree):
        self.tree = decision_tree
        self.estados_usuario = {}  # Almacena estados por usuario_id

    def avanzar(self, mensaje: str, usuario_id: str = "default"):
        # Si el estado del usuario no está en el diccionario, se inicializa
        if usuario_id not in self.estados_usuario:
            self.estados_usuario[usuario_id] = self.tree.root

        estado_actual = self.estados_usuario[usuario_id]
        entrada = mensaje.strip()

        siguiente = DecisionTreeService.get_node_by_option(estado_actual, entrada)
        if siguiente:
            self.estados_usuario[usuario_id] = siguiente
        # Permite volver al menú principal con palabras clave.
        elif entrada.lower() in ["volver", "inicio", "root"]:
            self.estados_usuario[usuario_id] = self.tree.root

        return self.estados_usuario[usuario_id]
