# Configuración de CORS para la aplicación FastAPI.
# Permite solicitudes desde cualquier origen y todos los métodos.
from fastapi.middleware.cors import CORSMiddleware


def configure_cors(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
