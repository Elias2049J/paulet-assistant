class HorarioClase:
    def __init__(
        self, curso: str, clase: str, tipo: str, desde: str, hasta: str, sede: str
    ):
        self.curso = curso
        self.clase = clase
        self.tipo = tipo
        self.desde = desde
        self.hasta = hasta
        self.sede = sede


class HorariosRedisData:
    def __init__(self, semana: str, dias: dict[str, list[HorarioClase]]):
        self.semana = semana
        self.dias = dias  # clave: día, valor: lista de HorarioClase
