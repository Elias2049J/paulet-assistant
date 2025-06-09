# Configuración de CORS para la aplicación FastAPI.
# Permite solicitudes POST desde cualquier origen.
from fastapi.middleware.cors import  CORSMiddleware


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["POST"],
        allow_headers=["*"],
    )
