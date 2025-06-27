from app.domain.entities.calificaciones.calificacion import Calificacion
from app.domain.entities.calificaciones.calificaciones_periodo import CalificacionesPeriodo
from typing import Union
import logging

logger = logging.getLogger(__name__)


def dict_to_calificacion(data: dict) -> Calificacion:
    """Convierte un diccionario de datos scrapeados a objeto Calificacion"""
    def safe_convert(value: str) -> Union[int, str]:
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return ""
        try:
            return int(str(value).strip())
        except (ValueError, TypeError):
            return str(value).strip()

    # Manejar tanto claves de scraping (Curso, Fórmula) como claves serializadas (curso, formula)
    # Primero buscar en formato scraping, luego en formato serializado
    curso = data.get("Curso", data.get("curso", "")).strip()
    formula = data.get("Fórmula", data.get("formula", "")).strip()
    vez = safe_convert(data.get("Vez", data.get("vez", "0")))
    t1 = safe_convert(data.get("T1", data.get("t1", "")))
    t2 = safe_convert(data.get("T2", data.get("t2", "")))
    t3 = safe_convert(data.get("T3", data.get("t3", "")))
    t4 = safe_convert(data.get("T4", data.get("t4", "")))
    t5 = safe_convert(data.get("T5", data.get("t5", "")))
    ep = safe_convert(data.get("EP", data.get("ep", "")))
    ef = safe_convert(data.get("EF", data.get("ef", "")))
    re = safe_convert(data.get("RE", data.get("re", "")))
    pf = safe_convert(data.get("PF", data.get("pf", "")))
    max_faltas = safe_convert(data.get("Max. Faltas", data.get("max_faltas", "")))
    faltas = safe_convert(data.get("Faltas", data.get("faltas", "")))

    # Log para depuración
    logger.debug(f"Creando objeto Calificacion: curso={curso}, pf={pf}, max_faltas={max_faltas}, faltas={faltas}")

    return Calificacion(
        curso=curso,
        formula=formula,
        vez=vez,
        t1=t1,
        t2=t2,
        t3=t3,
        t4=t4,
        t5=t5,
        ep=ep,
        ef=ef,
        re=re,
        pf=pf,
        max_faltas=max_faltas,
        faltas=faltas,
    )


def crear_calificaciones_por_periodo(periodo: str, calificaciones_data: list) -> CalificacionesPeriodo:
    try:
        # Añadir log para depuración
        logger.debug(f"Creando calificaciones para período {periodo} con {len(calificaciones_data)} elementos")
        if calificaciones_data and len(calificaciones_data) > 0:
            logger.debug(f"Primer elemento: {calificaciones_data[0]}")

        calificaciones = [dict_to_calificacion(c) for c in calificaciones_data]
        return CalificacionesPeriodo(periodo=periodo, calificaciones=calificaciones)
    except Exception as e:
        logger.error(f"Error al crear calificaciones para período {periodo}: {e}")
        # Devolver un objeto válido pero vacío en caso de error
        return CalificacionesPeriodo(periodo=periodo, calificaciones=[])
