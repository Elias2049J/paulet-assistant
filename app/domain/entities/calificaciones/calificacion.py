class Calificacion:
    def __init__(self, curso: str, formula: str, vez: int, t1: int, t2: int, t3: int, t4: str, t5: str, ep: int,
                 ef: int, re: int, pf: int, max_faltas: int, faltas: int):
        self._curso = curso
        self._formula = formula
        self._vez = vez
        self._t1 = t1
        self._t2 = t2
        self._t3 = t3
        self._t4 = t4
        self._t5 = t5
        self._ep = ep
        self._ef = ef
        self._re = re
        self._pf = pf
        self._max_faltas = max_faltas
        self._faltas = faltas

    @property
    def curso(self) -> str:
        return self._curso

    @curso.setter
    def curso(self, value: str):
        self._curso = value

    @property
    def formula(self) -> str:
        return self._formula

    @formula.setter
    def formula(self, value: str):
        self._formula = value

    @property
    def vez(self) -> int:
        return self._vez

    @vez.setter
    def vez(self, value: int):
        self._vez = value

    @property
    def t1(self) -> int:
        return self._t1

    @t1.setter
    def t1(self, value: int):
        self._t1 = value

    @property
    def t2(self) -> int:
        return self._t2

    @t2.setter
    def t2(self, value: int):
        self._t2 = value

    @property
    def t3(self) -> int:
        return self._t3

    @t3.setter
    def t3(self, value: int):
        self._t3 = value

    @property
    def t4(self) -> str:
        return self._t4

    @t4.setter
    def t4(self, value: str):
        self._t4 = value

    @property
    def t5(self) -> str:
        return self._t5

    @t5.setter
    def t5(self, value: str):
        self._t5 = value

    @property
    def ep(self) -> int:
        return self._ep

    @ep.setter
    def ep(self, value: int):
        self._ep = value

    @property
    def ef(self) -> int:
        return self._ef

    @ef.setter
    def ef(self, value: int):
        self._ef = value

    @property
    def re(self) -> int:
        return self._re

    @re.setter
    def re(self, value: int):
        self._re = value

    @property
    def pf(self) -> int:
        return self._pf

    @pf.setter
    def pf(self, value: int):
        self._pf = value

    @property
    def max_faltas(self) -> int:
        return self._max_faltas

    @max_faltas.setter
    def max_faltas(self, value: int):
        self._max_faltas = value

    @property
    def faltas(self) -> int:
        return self._faltas

    @faltas.setter
    def faltas(self, value: int):
        self._faltas = value

    def __str__(self):
        return (f"Curso: {self.curso}, Formula: {self.formula}, Vez: {self.vez}, "
                f"T1: {self.t1}, T2: {self.t2}, T3: {self.t3}, T4: {self.t4}, "
                f"T5: {self.t5}, EP: {self.ep}, EF: {self.ef}, RE: {self.re}, "
                f"PF: {self.pf}, Max Faltas: {self.max_faltas}, Faltas: {self.faltas}")

    def __todict__(self):
        return {
            "curso": self.curso,
            "formula": self.formula,
            "vez": self.vez,
            "t1": self.t1,
            "t2": self.t2,
            "t3": self.t3,
            "t4": self.t4,
            "t5": self.t5,
            "ep": self.ep,
            "ef": self.ef,
            "re": self.re,
            "pf": self.pf,
            "max_faltas": self.max_faltas,
            "faltas": self.faltas
        }
