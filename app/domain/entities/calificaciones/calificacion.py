from dataclasses import dataclass, asdict
from typing import Union


@dataclass
class Calificacion:
    curso: str
    formula: str
    vez: int
    t1: Union[int, str]
    t2: Union[int, str]
    t3: Union[int, str]
    t4: Union[int, str]
    t5: Union[int, str]
    ep: Union[int, str]
    ef: Union[int, str]
    re: Union[int, str]
    pf: Union[int, str]
    max_faltas: Union[int, str]
    faltas: Union[int, str]

    def to_dict(self):
        # Convertir a diccionario garantizando que ningún campo quede vacío
        result = {}
        for key, value in asdict(self).items():
            # Asegurar que los valores vacíos se convierten en cadenas vacías y no en None
            result[key] = value if value is not None else ""
        return result

    def __str__(self):
        return (f"Curso: {self.curso}, Formula: {self.formula}, Vez: {self.vez}, "
                f"T1: {self.t1}, T2: {self.t2}, T3: {self.t3}, T4: {self.t4}, "
                f"T5: {self.t5}, EP: {self.ep}, EF: {self.ef}, RE: {self.re}, "
                f"PF: {self.pf}, Max Faltas: {self.max_faltas}, Faltas: {self.faltas}")
