class HorarioSemanal:
    def __init__ (self, alumno: str,semana:str, horarios_diarios: list):
        self._alumno = alumno
        self._semana = semana
        self._horarios_diarios = horarios_diarios

    @property
    def alumno(self) -> str:
        return self._alumno

    @alumno.setter
    def alumno(self, value: str):
        self._alumno = value

    @property
    def semana(self) -> str:
        return self._semana

    @semana.setter
    def semana(self, value: str):
        self._semana = value

    @property
    def horarios_diarios(self) -> list:
        return self._horarios_diarios

    @horarios_diarios.setter
    def horarios_diarios(self, value: list):
        self._horarios_diarios = value

    def __str__(self):
        return f"Horario de la semana {self.semana}: " + ", ".join([str(horario_diario) for horario_diario in self.horarios_diarios])
