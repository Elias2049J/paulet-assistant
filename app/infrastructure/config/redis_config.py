# Configuración centralizada para Redis
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class RedisConfig:
    """Configuración para Redis con valores por defecto y validación"""
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: Optional[str] = None
    max_connections: int = 20
    socket_timeout: int = 5
    socket_connect_timeout: int = 5
    retry_on_timeout: bool = True
    health_check_interval: int = 30
    default_ttl: int = 3600  # 1 hora por defecto

    @classmethod
    def from_env(cls) -> 'RedisConfig':
        """Crea configuración desde variables de entorno"""
        return cls(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            db=int(os.getenv("REDIS_DB", "0")),
            password=os.getenv("REDIS_PASSWORD"),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "20")),
            socket_timeout=int(os.getenv("REDIS_SOCKET_TIMEOUT", "5")),
            socket_connect_timeout=int(os.getenv("REDIS_CONNECT_TIMEOUT", "5")),
            retry_on_timeout=os.getenv("REDIS_RETRY_ON_TIMEOUT", "true").lower() == "true",
            health_check_interval=int(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", "30")),
            default_ttl=int(os.getenv("REDIS_DEFAULT_TTL", "3600"))
        )

    def validate(self) -> bool:
        """Valida la configuración"""
        if not isinstance(self.port, int) or self.port <= 0 or self.port > 65535:
            raise ValueError(f"Puerto Redis inválido: {self.port}")

        if not isinstance(self.db, int) or self.db < 0:
            raise ValueError(f"Base de datos Redis inválida: {self.db}")

        if self.max_connections <= 0:
            raise ValueError("max_connections debe ser mayor que 0")

        if self.socket_timeout <= 0:
            raise ValueError("socket_timeout debe ser mayor que 0")

        if self.default_ttl <= 0:
            raise ValueError("default_ttl debe ser mayor que 0")

        return True

    def get_connection_url(self) -> str:
        """Genera URL de conexión para Redis"""
        auth = f":{self.password}@" if self.password else ""
        return f"redis://{auth}{self.host}:{self.port}/{self.db}"

# Configuración global
redis_config = RedisConfig.from_env()
redis_config.validate()
