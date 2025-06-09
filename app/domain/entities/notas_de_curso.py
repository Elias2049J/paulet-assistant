# Entidad que representa las notas y faltas asociadas a un curso específico.
from app.domain.entities.nota import Nota
from app.domain.entities.curso import Curso
from app.domain.entities.faltas import Faltas


class NotasDeCurso:
    def __init__(self, curso: Curso, notas: dict[str, Nota], faltas: Faltas):
        self.curso = curso  # Instancia de Curso
        self.notas = notas  # Diccionario de notas por evaluación
        self.faltas = faltas  # Instancia de Faltas asociada al curso
