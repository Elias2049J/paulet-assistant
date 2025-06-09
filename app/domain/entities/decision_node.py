# Entidad que representa un nodo del árbol de decisiones del flujo conversacional.
class DecisionNode:
    def __init__(
        self, mensaje: str,
            opciones: dict = None,
            accion: str = None, 
            padre=None
    ):
        self.mensaje = mensaje  # Mensaje a mostrar al usuario
        self.opciones = opciones if opciones else {}  # Opciones de respuesta
        self.accion = accion  # Acción a ejecutar en este nodo (si aplica)
        self.padre = padre  # Nodo padre (para volver atrás)

    def get_mensaje(self) -> str:
        return self.mensaje

    def get_opciones(self) -> dict:
        return self.opciones

    def get_accion(self) -> str:
        return self.accion

    def get_padre(self):
        return self.padre
