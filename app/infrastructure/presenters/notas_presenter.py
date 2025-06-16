# formatea la respuesta del scraper de notas
# recibe una lista de dicts con cursos, notas y faltas, y devuelve un string legible
class NotasPresenter:
    @staticmethod
    def formatear_respuesta(notas, ciclo, desde_cache=False):
        origen = "(desde caché)" if desde_cache else "(desde scraping)"
        if not notas:
            return f"{origen} No se encontraron notas para el ciclo {ciclo}."

        # extrae encabezado
        encabezados = list(notas[0].keys())
        # construye el encabezado
        cabecera = "\t".join(encabezados)

        lineas = [f"Notas para {notas[0].get('usuario', 'usuario')} en ciclo {ciclo}:", cabecera]
        # construir filas
        for n in notas:
            fila = "\t".join(str(n.get(col, "")) for col in encabezados)
            lineas.append(fila)
            # añade opción para volver en la respuesta
        lineas.append("1. Volver a las opciones")
        return f"{origen} " + "\n".join(lineas)
