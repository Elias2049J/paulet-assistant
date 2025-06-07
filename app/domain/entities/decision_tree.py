from app.domain.entities.decision_node import DecisionNode


class DecisionTree:
    def __init__(self):
        self.root = DecisionNode(
            mensaje="Hola, soy Paulet, tu asistente virtual. Escoge una de las siguientes opciones:"
            + "\n1. Consultar notas.\n2. Consultar horarios.",
            opciones={},
        )

        self.notas_menu = DecisionNode(
            mensaje="Genial! ¿Deseas las notas de este ciclo o de algún otro?"
            + "\n1. Ciclo en curso\n2. Otro ciclo\n3. Volver a las opciones",
            opciones={},
        )

        self.opcion_notas = DecisionNode(
            mensaje="(desde árbol) Mostrando tus notas del ciclo en curso...",
            accion="consultar_notas",
        )

        # Nodo de acción: al consultar notas, hace acción y luego muestra menú para volver
        self.resultado_notas = DecisionNode(
            mensaje="",  # el mensaje se construye dinámicamente
            accion="consultar_notas",
            opciones={},  # se agregará abajo
        )

        self.resultado_horarios = DecisionNode(
            mensaje="", accion="consultar_horarios", opciones={}
        )

        self.volver = self.root  # reutilizamos el nodo raíz

        self.opcion_otro_ciclo = DecisionNode(
            mensaje="Por ahora solo tengo acceso al ciclo en curso.\n1. Volver a las opciones",
            opciones={"1": self.root},
        )

        self.root.opciones = {"1": self.notas_menu, "2": self.resultado_horarios}
        self.notas_menu.opciones = {
            "1": self.resultado_notas,
            "2": self.opcion_otro_ciclo,
            "3": self.root,
        }
        self.resultado_notas.opciones = {"1": self.root}
        self.resultado_horarios.opciones = {"1": self.root}

    def get_root(self) -> DecisionNode:
        return self.root

    def evaluate(self, input: str) -> DecisionNode:
        return self.root.get_opciones().get(input.strip(), self.root)
