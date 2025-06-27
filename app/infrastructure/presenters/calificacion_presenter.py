class CalificacionPresenter:
    @staticmethod
    def formatear_respuesta(periodos, ciclo, desde_cache=False):
        origen = "(desde caché)" if desde_cache else "(desde scraping)"
        if not periodos:
            return f"{origen} No se encontraron notas para el ciclo {ciclo}."

        lineas = [f"{origen} Notas para el ciclo {ciclo}:"]

        for periodo_key, periodo_obj in periodos.items():
            lineas.append(f"\n📅 Período {periodo_obj.periodo}:")
            for cal in periodo_obj.calificaciones:
                # Mostrar curso con nota final y faltas
                pf_texto = cal.pf if cal.pf != "" else "Sin nota"
                faltas_texto = f"{cal.faltas}/{cal.max_faltas}" if cal.max_faltas != "" else "N/A"
                lineas.append(f"  • {cal.curso}: {pf_texto} (faltas: {faltas_texto})")

        # No añadir opciones de navegación aquí, solo mostrar los datos
        return "\n".join(lineas)

    @staticmethod
    def formatear_respuesta_periodo(periodo_obj, periodo_id):
        """Formatea la respuesta para un período específico incluyendo opciones de navegación"""
        if not periodo_obj or not periodo_obj.calificaciones:
            return f"No se encontraron notas para el período {periodo_id}."

        lineas = [f"Notas del período {periodo_id}:"]

        for cal in periodo_obj.calificaciones:
            # Mostrar curso con nota final y faltas
            pf_texto = cal.pf if cal.pf != "" else "Sin nota"
            faltas_texto = f"{cal.faltas}/{cal.max_faltas}" if cal.max_faltas != "" else "N/A"
            nombre_curso = cal.curso if cal.curso and cal.curso.strip() else "Curso sin nombre"
            lineas.append(f"  • {nombre_curso}: {pf_texto} (faltas: {faltas_texto})")

        # Añadir opciones de navegación
        lineas.append("\n1. Seleccionar otro período")
        lineas.append("2. Volver al menú principal")

        return "\n".join(lineas)
