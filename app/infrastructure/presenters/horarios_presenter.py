class HorariosPresenter:
    @staticmethod
    def formatear_respuesta(horarios, ciclo, desde_cache=False):
        origen = "(desde caché)" if desde_cache else "(desde scraping)"

        if isinstance(horarios, str):
            return f"{origen} {horarios}"

        resultado = [f"{origen} Horarios para ciclo {ciclo}:"]

        for dia, clases in horarios.items():
            resultado.append(f"\{dia}:")
            for clase in clases:
                resultado.append(f"  • {clase['curso']} - {clase['desde']} a {clase['hasta']} - {clase['sede']}")

        resultado.append("\1. Volver a las opciones")
        return "\n".join(resultado)