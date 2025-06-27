class DecisionNode:
    def __init__(self, mensaje: str, opciones: dict = None, accion: str = None, padre=None):
        self._mensaje = mensaje
        self._opciones = opciones if opciones else {}
        self._accion = accion
        self._padre = padre

    @property
    def mensaje(self) -> str:
        return self._mensaje

    @mensaje.setter
    def mensaje(self, value: str):
        self._mensaje = value

    @property
    def opciones(self) -> dict:
        return self._opciones

    @opciones.setter
    def opciones(self, value: dict):
        self._opciones = value

    @property
    def accion(self) -> str:
        return self._accion

    @accion.setter
    def accion(self, value: str):
        self._accion = value


    @property
    def padre(self):
        return self._padre

    @padre.setter
    def padre(self, value):
        self._padre = value

    def __str__(self):
        return f"DecisionNode(mensaje={self.mensaje}, opciones={self.opciones}, accion={self.accion})"
