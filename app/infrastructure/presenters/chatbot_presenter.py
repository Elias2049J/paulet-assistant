class ChatbotPresenter:
    def __init__(self, service):
        self.service = service

    async def manejar_entrada_de_usuario(self, mensaje: str, usuario_id: str = "default") -> str:
        """Método para transformar entrada del usuario en respuesta"""
        return await self.service.procesar_consulta(mensaje, usuario_id)
