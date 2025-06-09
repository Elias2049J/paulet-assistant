# Entidad que representa las faltas de un curso.
class Faltas:
    def __init__(self, maximas: int, actuales: int):
        self.maximas = maximas  # Número máximo de faltas permitidas
        self.actuales = actuales  # Número actual de faltas
