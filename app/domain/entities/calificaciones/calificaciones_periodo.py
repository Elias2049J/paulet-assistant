from dataclasses import dataclass, field
from typing import List
from .calificacion import Calificacion


@dataclass
class CalificacionesPeriodo:
    periodo: str
    calificaciones: List[Calificacion] = field(default_factory=list)

    def __str__(self):
        return f"Calificaciones del periodo {self.periodo}: " + ", ".join([str(cal) for cal in self.calificaciones])
