import os
from cryptography.fernet import Fernet
import logging

logger = logging.getLogger(__name__)


class AuthLoader:
    """
    Centraliza la obtención y descifrado de credenciales de usuario y password desde Redis.
    """
    @staticmethod
    def get_fernet():
        FERNET_KEY = os.getenv("FERNET_KEY")
        if not FERNET_KEY:
            logger.error("FERNET_KEY no definida en el entorno.")
            raise RuntimeError("FERNET_KEY debe estar definida en el entorno para descifrar credenciales.")
        return Fernet(FERNET_KEY)

    @staticmethod
    def get_credentials(redis):
        usuario_encrypted = redis.get("USUARIO")
        password_encrypted = redis.get("PASSWORD")
        if not usuario_encrypted or not password_encrypted:
            logger.error("Credenciales USUARIO y PASSWORD no encontradas en Redis.")
            raise ValueError("Faltan credenciales en Redis. El usuario debe autenticarse primero.")
        fernet = AuthLoader.get_fernet()
        try:
            usuario = fernet.decrypt(usuario_encrypted.encode()).decode()
            password = fernet.decrypt(password_encrypted.encode()).decode()
            return usuario, password
        except Exception as e:
            logger.error(f"Error descifrando credenciales: {e}")
            raise ValueError("No se pudieron descifrar las credenciales de usuario/password desde Redis.")

