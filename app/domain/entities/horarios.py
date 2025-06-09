# Entidad que representa un horario de clase y la estructura semanal de horarios.
class Horario:
    def __init__(
        self, curso: str, clase: str, tipo: str, desde: str, hasta: str, sede: str
    ):
        self.curso = curso  # Nombre del curso
        self.clase = clase  # Nombre de la clase
        self.tipo = tipo    # Tipo de clase (teoría, práctica, etc.)
        self.desde = desde  # Hora de inicio
        self.hasta = hasta  # Hora de fin
        self.sede = sede    # Sede o aula


class HorariosData:
    def __init__(self, semana: str, dias: dict[str, list[Horario]]):
        self.semana = semana  # Semana académica
        self.dias = dias      # clave: día, valor: lista de Horario
