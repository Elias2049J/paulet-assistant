class DecisionNode:
    def __init__(
        self, mensaje: str, opciones: dict = None, accion: str = None, padre=None
    ):
        self.mensaje = mensaje
        self.opciones = opciones if opciones else {}
        self.accion = accion
        self.padre = padre

    def get_mensaje(self) -> str:
        return self.mensaje

    def get_opciones(self) -> dict:
        return self.opciones

    def get_accion(self) -> str:
        return self.accion

    def get_padre(self):
        return self.padre
