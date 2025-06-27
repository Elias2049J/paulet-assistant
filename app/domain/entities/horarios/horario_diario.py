from dataclasses import dataclass, field
from typing import List
from .horario_curso import Curso

@dataclass
class HorarioDiario:
    dia: str
    cursos: List[Curso] = field(default_factory=list)

    def __str__(self):
        return f"Horario del {self.dia}: " + ", ".join([str(curso) for curso in self.cursos])