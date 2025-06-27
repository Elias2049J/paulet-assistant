from app.application.interfaces.flow_manager_interface import FlowManagerInterface
from app.application.interfaces.chatbot_interface import ChatbotInterface
from app.infrastructure.presenters.horarios_presenter import HorariosPresenter
from app.infrastructure.presenters.notas_presenter import NotasPresenter


class ChatbotService(ChatbotInterface):
    def __init__(self, flow_manager: FlowManagerInterface, use_cases):
        self.flow_manager = flow_manager
        self.use_cases = use_cases
        self.presenters = {
            "consultar_notas": NotasPresenter,
            "consultar_horarios": HorariosPresenter
        }

    def procesar_consulta(self, mensaje: str, usuario_id: str = "default") -> str:
        # Usa los datos del usuario ya definidos en main.py a través de los use_cases y scrapers
        estado = self.flow_manager.avanzar(mensaje, usuario_id)
        accion = estado.get_accion()

        if accion and accion in self.use_cases:
            datos, ciclo, desde_cache = self.use_cases[accion].ejecutar_consulta()
            if accion in self.presenters:
                return self.presenters[accion].formatear_respuesta(datos, ciclo, desde_cache)
            else:
                return str(datos) # para operaciones sin presentador
        return estado.get_mensaje()
