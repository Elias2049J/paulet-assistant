import json

from app.application.factory.decision_tree_factory import DecisionTreeFactory
from app.domain.entities.decision_tree.decision_tree import DecisionTree


class DecisionTreeLoader:
    @staticmethod
    def cargar_desde_archivo(config_path='decision_tree.json') -> dict:
        with open(config_path, encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def crear_arbol_decisiones(config_path='decision_tree.json') -> DecisionTree:
        config_data = DecisionTreeLoader.cargar_desde_archivo(config_path)
        return DecisionTreeFactory.create_from_config(config_data)
