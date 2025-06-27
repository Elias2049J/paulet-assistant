class Curso:
    def __init__(
        self, curso: str, clase: str, tipo_clase: str, aula: str, hora_inicio: str, hora_fin: str, sede: str
    ):
        self._curso = curso
        self._clase = clase
        self._tipo_clase = tipo_clase
        self._aula = aula
        self._hora_inicio = hora_inicio
        self._hora_fin = hora_fin
        self._sede = sede

    @property
    def curso(self) -> str:
        return self._curso

    @curso.setter
    def curso(self, value: str):
        self._curso = value

    @property
    def clase(self) -> str:
        return self._clase

    @clase.setter
    def clase(self, value: str):
        self._clase = value

    @property
    def tipo_clase(self) -> str:
        return self._tipo_clase

    @tipo_clase.setter
    def tipo_clase(self, value: str):
        self._tipo_clase = value

    @property
    def aula(self) -> str:
        return self._aula

    @aula.setter
    def aula(self, value: str):
        self._aula = value

    @property
    def hora_inicio(self) -> str:
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, value: str):
        self._hora_inicio = value

    @property
    def hora_fin(self) -> str:
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, value: str):
        self._hora_fin = value

    @property
    def sede(self) -> str:
        return self._sede

    @sede.setter
    def sede(self, value: str):
        self._sede = value

    def __str__(self):
        return (
            f"Curso: {self.curso}, Clase: {self.clase}, Tipo: {self.tipo_clase}, "
            f"Aula: {self.aula}, Hora Inicio: {self.hora_inicio}, Hora Fin: {self.hora_fin}, Sede: {self.sede}"
        )
