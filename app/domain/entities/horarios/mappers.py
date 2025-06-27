from app.domain.entities.horarios.horario_curso import Curso
from app.domain.entities.horarios.horario_diario import HorarioDiario
import logging

logger = logging.getLogger(__name__)


def dict_to_curso(data) -> Curso:
    """
    Convierte un diccionario o string a un objeto Curso.
    Maneja correctamente diferentes formatos de entrada.
    """
    try:
        # Si es un diccionario, extraer los valores
        if isinstance(data, dict):
            return Curso(
                curso=data.get("curso", ""),
                clase=data.get("clase", ""),
                tipo_clase=data.get("tipo_clase", ""),
                aula=data.get("aula", ""),
                hora_inicio=data.get("desde", ""),
                hora_fin=data.get("hasta", ""),
                sede=data.get("sede", "")
            )
        # Si es una cadena, crear un curso con solo el nombre
        elif isinstance(data, str):
            logger.warning(f"Recibido string en lugar de diccionario para curso: {data}")
            return Curso(curso=data)
        # Si es otro tipo, crear un curso vacío
        else:
            logger.error(f"Tipo de datos inesperado para curso: {type(data)}")
            return Curso(curso="Error: formato no válido")
    except Exception as e:
        logger.error(f"Error convirtiendo datos a Curso: {e}")
        return Curso(curso="Error: " + str(e))


def dict_to_horario_diario(dia: str, cursos_data) -> HorarioDiario:
    """
    Convierte una lista de cursos a un objeto HorarioDiario.
    Maneja correctamente diferentes formatos de entrada.
    """
    try:
        # Verificar si cursos_data es una lista
        if not isinstance(cursos_data, list):
            logger.warning(f"cursos_data para {dia} no es una lista: {type(cursos_data)}")
            if isinstance(cursos_data, str) or cursos_data is None:
                return HorarioDiario(dia, [])
            try:
                # Intentar convertir a lista si es posible
                cursos_data = list(cursos_data)
            except:
                return HorarioDiario(dia, [])

        # Convertir cada curso
        cursos = []
        for c in cursos_data:
            try:
                cursos.append(dict_to_curso(c))
            except Exception as e:
                logger.error(f"Error convirtiendo curso para {dia}: {e}")

        return HorarioDiario(dia, cursos)
    except Exception as e:
        logger.error(f"Error procesando horario para día {dia}: {e}")
        return HorarioDiario(dia, [])
