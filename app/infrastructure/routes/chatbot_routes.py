# Archivo de rutas para el chatbot. Define el endpoint principal de la API REST que recibe mensajes del usuario y
# retorna la respuesta del asistente virtual. Se encarga de recibir la petición HTTP, extraer el mensaje y delegar el
# procesamiento al presentador.

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# Modelo de datos para la petición del usuario.
# Solo requiere el campo 'message' que contiene el texto enviado por el usuario.
class ChatRequest(BaseModel):
    message: str


# Función para registrar la ruta del chatbot en la aplicación FastAPI.
# Recibe el presentador y define el endpoint POST '/paulet/chat'.
def get_router(presenter):
    @router.post("/paulet/chat")
    async def conversar(request: ChatRequest):
        # Delegamos el procesamiento del mensaje al presentador.
        respuesta = presenter.manejar_entrada_de_usuario(request.message)
        return {"respuesta": respuesta}

    return router
