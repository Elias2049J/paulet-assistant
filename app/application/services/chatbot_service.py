from app.application.interfaces.flow_manager_interface import FlowManagerInterface
from app.application.interfaces.chatbot_interface import ChatbotInterface
from app.infrastructure.presenters.notas_presenter import NotasPresenter


class ChatbotService(ChatbotInterface):
    def __init__(self, flow_manager: FlowManagerInterface, use_cases):
        self.flow_manager = flow_manager
        self.use_cases = use_cases

    def procesar_consulta(self, mensaje: str) -> str:
        # Usa los datos del usuario ya definidos en main.py a través de los use_cases y scrapers
        estado = self.flow_manager.avanzar(mensaje)
        accion = estado.get_accion()
        if accion and accion in self.use_cases:
            if accion == "consultar_notas":
                notas, ciclo, desde_cache = self.use_cases[accion].ejecutar_consulta()
                return NotasPresenter.formatear_respuesta(notas, ciclo, desde_cache)
            else:
                return self.use_cases[accion].ejecutar_consulta()
        return estado.get_mensaje()
