import logging

logger = logging.getLogger(__name__)


class HorariosPresenter:
    @staticmethod
    def formatear_respuesta(horarios, desde_cache=False):
        origen = "(desde caché)" if desde_cache else "(desde scraping)"
        logger.info(f"Origen de datos de horarios: {origen}")

        if isinstance(horarios, str):
            return f"{origen} {horarios}"

        resultado = [f"Horarios:"]

        # Verificar si hay horarios con cursos reales
        total_cursos = 0
        cursos_validos = 0

        # Contar solo cursos válidos con nombre del curso
        for dia, horario_diario in horarios.items():
            for curso in horario_diario.cursos:
                total_cursos += 1
                if (curso.curso and
                    not curso.curso.isdigit() and  # Evitar que períodos (números) se cuenten como cursos
                    curso.curso not in ["Error: formato no válido", "periodos"]):
                    cursos_validos += 1

        # Si no hay cursos reales en total, mostrar un mensaje
        if cursos_validos == 0:
            return f"No se encontraron horarios disponibles. Por favor intenta más tarde."

        # Mostrar solo días con cursos válidos
        for dia, horario_diario in horarios.items():
            # Filtrar solo cursos válidos para este día
            cursos_validos_dia = [
                curso for curso in horario_diario.cursos
                if curso.curso and
                   not curso.curso.isdigit() and  # Evitar períodos como cursos
                   curso.curso not in ["Error: formato no válido", "periodos"]
            ]

            # Solo mostrar días que tienen cursos válidos
            if cursos_validos_dia:
                resultado.append(f"\n📅 {dia}:")
                for clase in cursos_validos_dia:
                    horario = f"{clase.hora_inicio}-{clase.hora_fin}" if clase.hora_inicio and clase.hora_fin else "Sin horario"
                    sede = clase.sede if clase.sede else "Sin sede"
                    aula = f" - {clase.aula}" if clase.aula else ""
                    resultado.append(f"  • {clase.curso} {horario} {sede}{aula}")

        # Agregar una sola opción para volver al menú principal
        resultado.append("\n1. Volver al menú principal")
        return "\n".join(resultado)
