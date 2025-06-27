from fastapi import APIRouter
from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str


def get_router(controller):
    router = APIRouter()

    @router.post("/paulet/chat")
    async def chat_endpoint(request: ChatRequest):
        respuesta = await controller.manejar_entrada_de_usuario(request.message)
        return {"respuesta": respuesta}

    return router