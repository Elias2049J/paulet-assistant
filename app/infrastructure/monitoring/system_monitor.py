import psutil
import logging

logger = logging.getLogger(__name__)

class SystemMonitor:
    @staticmethod
    def get_memory_usage():
        """
        Obtiene el uso actual de memoria del proceso en MB.

        Returns:
            dict: Diccionario con información sobre el uso de memoria
        """
        process = psutil.Process()
        memory_info = process.memory_info()

        memory_usage = {
            "rss": round(memory_info.rss / (1024 * 1024), 2),  # Resident Set Size en MB
            "vms": round(memory_info.vms / (1024 * 1024), 2),  # Virtual Memory Size en MB
            "percent": process.memory_percent(),
            "system_total": round(psutil.virtual_memory().total / (1024 * 1024), 2),  # Total en MB
            "system_available": round(psutil.virtual_memory().available / (1024 * 1024), 2)  # Disponible en MB
        }

        logger.info(f"Uso de memoria: {memory_usage['rss']} MB (RSS), {memory_usage['percent']}% del proceso")

        return memory_usage

    @staticmethod
    def log_system_resources():
        """
        Registra información sobre los recursos del sistema.
        """
        # Información de CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)

        # Información de memoria
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = round(memory.used / (1024 * 1024), 2)  # MB
        memory_total = round(memory.total / (1024 * 1024), 2)  # MB

        # Información del proceso actual
        process = psutil.Process()
        process_memory = round(process.memory_info().rss / (1024 * 1024), 2)  # MB
        process_cpu = process.cpu_percent(interval=0.1)

        logger.info(f"Sistema - CPU: {cpu_percent}%, Memoria: {memory_used}/{memory_total} MB ({memory_percent}%)")
        logger.info(f"Proceso - CPU: {process_cpu}%, Memoria: {process_memory} MB")

        return {
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "memory_used_mb": memory_used,
                "memory_total_mb": memory_total
            },
            "process": {
                "cpu_percent": process_cpu,
                "memory_mb": process_memory
            }
        }
