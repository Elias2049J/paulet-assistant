class HorarioDiario:
    def __init__(self, dia: str, cursos: list):
        self._dia = dia
        self._cursos = cursos

    @property
    def dia(self) -> str:
        return self._dia

    @dia.setter
    def dia(self, value: str):
        self._dia = value

    @property
    def cursos(self) -> list:
        return self._cursos

    @cursos.setter
    def cursos(self, value: list):
        self._cursos = value

    def __str__(self):
        return f"Horario del {self.dia}: " + ", ".join([str(curso) for curso in self.cursos])