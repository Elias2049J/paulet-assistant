from typing import Any

from app.domain.entities.decision_tree.decision_node import DecisionNode
from app.domain.entities.decision_tree.decision_tree import DecisionTree


class DecisionTreeService:
    @staticmethod
    def crear_desde_archivo(config_data: dict) -> DecisionTree:
        nodos = {}

        for clave, valor in config_data.items():
            nodos[clave] = DecisionNode(
                mensaje=valor.get('mensaje', ''),
                accion=valor.get('accion'),
                opciones={}
            )

        for clave, valor in config_data.items():
            opciones = valor.get('opciones', {})
            nodos[clave].opciones = {k: nodos[v] for k, v in opciones.items()}

        return DecisionTree(nodos['root'])

    @staticmethod
    def get_node_by_option(nodo_actual: DecisionNode, opcion: str) -> DecisionNode | None:
        if opcion in nodo_actual.opciones:
            return nodo_actual.opciones[opcion]
        return None
