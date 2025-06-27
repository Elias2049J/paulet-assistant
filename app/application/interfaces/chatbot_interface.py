from abc import ABC, abstractmethod


class ChatbotInterface(ABC):
    @abstractmethod
    def procesar_consulta(self, mensaje: str, usuario_id: str = "default") -> str:
        # Procesa una consulta del usuario y retorna la respuesta.
        pass