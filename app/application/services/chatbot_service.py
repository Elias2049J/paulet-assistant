from app.application.interfaces.flow_manager_interface import FlowManagerInterface
from app.application.interfaces.chatbot_interface import ChatbotInterface


class ChatbotService(ChatbotInterface):
    def __init__(self, flow_manager: FlowManagerInterface, use_cases):
        self.flow_manager = flow_manager
        self.use_cases = use_cases

    def procesar_consulta(self, mensaje: str) -> str:
        # Usa los datos fijos ya definidos en main.py a través de los use_cases y scrapers
        estado = self.flow_manager.avanzar(mensaje)
        accion = estado.get_accion()
        if accion and accion in self.use_cases:
            return self.use_cases[accion].ejecutar_consulta()
        return estado.get_mensaje()
