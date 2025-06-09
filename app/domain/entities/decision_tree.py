# Entidad que representa el árbol de decisiones para el flujo conversacional.
# Carga la configuración desde un archivo JSON y enlaza los nodos.
import json
from app.domain.entities.decision_node import DecisionNode


class DecisionTree:
    def __init__(self, config_path='decision_tree.json'):
        with open(config_path, encoding='utf-8') as f:
            data = json.load(f)
        self.nodes = {}
        # Crea nodos sin opciones
        for key, value in data.items():
            self.nodes[key] = DecisionNode(
                mensaje=value.get('mensaje', ''),
                accion=value.get('accion'),
                opciones={}
            )
        # Enlaza opciones entre nodos
        for key, value in data.items():
            opciones = value.get('opciones', {})
            self.nodes[key].opciones = {k: self.nodes[v] for k, v in opciones.items()}
        self.root = self.nodes['root']

    def get_root(self):
        return self.root
