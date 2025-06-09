# Interfaz para el gestor de flujo conversacional en Clean Architecture.
# Define el método que debe implementar cualquier gestor de flujo.
from abc import ABC, abstractmethod


class FlowManagerInterface(ABC):
    @abstractmethod
    def avanzar(self, mensaje: str):
        # Avanza el flujo conversacional según el mensaje del usuario.
        pass