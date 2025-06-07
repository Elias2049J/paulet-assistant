from fastapi import APIRouter
from api.controllers.chatbot_controller import ChatbotController

router = APIRouter()
controller = ChatbotController()


@router.get("/paulet/{mensaje}")
async def conversar(mensaje: str):
    respuesta = controller.handle_user_input(mensaje)
    return {"respuesta": respuesta}
