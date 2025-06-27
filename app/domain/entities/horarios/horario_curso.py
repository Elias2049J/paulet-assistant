from dataclasses import dataclass, asdict

@dataclass
class Curso:
    curso: str
    clase: str = ""
    tipo_clase: str = ""
    aula: str = ""
    hora_inicio: str = ""
    hora_fin: str = ""
    sede: str = ""

    def to_dict(self):
        return asdict(self)

    def __str__(self):
        return (f"Curso: {self.curso}, Clase: {self.clase}, Tipo: {self.tipo_clase}, "
                f"Aula: {self.aula}, Hora Inicio: {self.hora_inicio}, Hora Fin: {self.hora_fin}, Sede: {self.sede}")
