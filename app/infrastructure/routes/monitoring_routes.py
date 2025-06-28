from fastapi import APIRouter, Depends
from app.infrastructure.monitoring.system_monitor import SystemMonitor

router = APIRouter(
    prefix="/monitor",
    tags=["monitoring"],
    responses={404: {"description": "No encontrado"}},
)


@router.get("/resources")
async def get_system_resources():
    """
    Endpoint para obtener información sobre los recursos del sistema.
    """
    return SystemMonitor.log_system_resources()


@router.get("/memory")
async def get_memory_usage():
    """
    Endpoint para obtener información específica sobre el uso de memoria.
    """
    return SystemMonitor.get_memory_usage()
