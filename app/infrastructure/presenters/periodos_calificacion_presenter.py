class PeriodosCalificacionPresenter:
    @staticmethod
    def formatear_respuesta(periodos, desde_cache=False):
        origen = "(desde caché)" if desde_cache else "(desde scraping)"

        if not periodos:
            return f"{origen} No se encontraron períodos disponibles."

        lineas = [f"{origen} Períodos disponibles para consultar notas:"]

        for i, periodo in enumerate(periodos, 1):
            lineas.append(f"{i}. Período {periodo}")

        lineas.append(f"{len(periodos) + 1}. Volver al menú principal")

        return "\n".join(lineas)
