from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.infrastructure.consultas.scrapers.login_playwright import LoginPlaywright
import json
from cryptography.fernet import Fernet
import os


class ChatRequest(BaseModel):
    message: str


class LoginRequest(BaseModel):
    username: str
    password: str


FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY debe estar definida en el entorno para encriptar credenciales.")
fernet = Fernet(FERNET_KEY)


def get_router(controller, redis=None):
    router = APIRouter()

    @router.post("/paulet/chat")
    async def chat_endpoint(request: ChatRequest):
        respuesta = await controller.manejar_entrada_de_usuario(request.message)
        return {"respuesta": respuesta}

    @router.post("/paulet/login")
    async def paulet_login(request: LoginRequest):
        username = request.username.strip()
        password = request.password.strip()
        if not username or not password:
            raise HTTPException(status_code=400, detail="Usuario y contraseña requeridos")

        try:
            login_checker = LoginPlaywright(redis, username, password)
            login_ok = await login_checker.login()
            if not login_ok:
                raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")
        except Exception as e:
            raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

        # Cifrar usuario y contraseña antes de guardarlas
        usuario_encrypted = fernet.encrypt(username.encode()).decode()
        password_encrypted = fernet.encrypt(password.encode()).decode()
        redis.set("USUARIO", usuario_encrypted, ex=60*60*8)
        redis.set("PASSWORD", password_encrypted, ex=60*60*8)
        session_data = {
            "usuario": username
        }
        try:
            if redis is None:
                raise HTTPException(status_code=500, detail="Redis no configurado")
            redis.set(f"session:{username}", json.dumps(session_data), ex=60*60*8)  # 8 horas
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error guardando sesión en Redis")

        return {"usuario": username, "login": True}

    return router
