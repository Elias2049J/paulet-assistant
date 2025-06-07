from app.use_cases.chatbot_service import ChatbotService


class ChatbotController:
    def __init__(self):
        self.service = ChatbotService()

    def handle_user_input(self, mensaje: str) -> str:
        return self.service.process_query(mensaje)
