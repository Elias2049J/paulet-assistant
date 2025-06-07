class NotasRedisData:
    def __init__(
        self, curso: str, notas: dict[str, int], faltas_max: int, faltas_actual: int
    ):
        self.curso = curso
        self.notas = notas
        self.faltas_max = faltas_max
        self.faltas_actual = faltas_actual
