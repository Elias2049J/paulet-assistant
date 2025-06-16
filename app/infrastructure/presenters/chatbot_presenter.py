# Presentador que conecta el servicio del chatbot con la capa de rutas (API REST).
# Solo recibe el mensaje y lo pasa al servicio.
class ChatbotPresenter:
    def __init__(self, service):
        self.service = service

    async def manejar_entrada_de_usuario(self, mensaje: str) -> str:
        return await self.service.procesar_consulta(mensaje)
