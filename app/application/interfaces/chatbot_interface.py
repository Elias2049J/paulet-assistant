# Interfaz para el servicio de chatbot en Clean Architecture.
# Define el método que debe implementar cualquier chatbot service.
from abc import ABC, abstractmethod


class ChatbotInterface(ABC):
    @abstractmethod
    async def procesar_consulta(self, mensaje: str) -> str:
        # Procesa una consulta del usuario y retorna la respuesta.
        pass