from app.domain.entities.decision_tree import DecisionTree
from app.use_cases.consultar_notas import ConsultarNotasUseCase
from app.use_cases.consultar_horarios import ConsultarHorariosUseCase


class ChatbotService:
    def __init__(self):
        self.tree = DecisionTree()
        self.estado_actual = self.tree.get_root()
        self.usuario = "usuario_demo"
        self.clave = "123456"
        self.ciclo = "2025-1"

    def process_query(self, mensaje: str) -> str:
        siguiente = self.estado_actual.get_opciones().get(mensaje.strip())

        if siguiente:
            self.estado_actual = siguiente
            if siguiente.get_accion() == "consultar_notas":
                return ConsultarNotasUseCase(
                    self.usuario, self.clave, self.ciclo
                ).ejecutar()
            elif siguiente.get_accion() == "consultar_horarios":
                return ConsultarHorariosUseCase(
                    self.usuario, self.clave, self.ciclo
                ).ejecutar()
            return siguiente.get_mensaje()

        # Si la entrada no es válida, no cambia de estado
        return self.estado_actual.get_mensaje()
