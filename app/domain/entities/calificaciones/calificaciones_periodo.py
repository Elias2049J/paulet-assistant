class CalificacionesPeriodo:
    def __init__(self, periodo: str, calificaciones: list):
        self.periodo = periodo
        self.calificaciones = calificaciones

    @property
    def periodo(self) -> str:
        return self._periodo

    @periodo.setter
    def periodo(self, value: str):
        self._periodo = value

    @property
    def calificaciones(self) -> list:
        return self._calificaciones

    @calificaciones.setter
    def calificaciones(self, value: list):
        self._calificaciones = value

    def __str__(self):
        return f"Calificaciones del periodo {self.periodo}: " + ", ".join([str(calificacion) for calificacion in self.calificaciones])
