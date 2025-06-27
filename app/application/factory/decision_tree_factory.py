from app.application.services.decision_tree_service import DecisionTreeService
from app.domain.entities.decision_tree.decision_tree import DecisionTree


class DecisionTreeFactory:
    @staticmethod
    def create_from_config(config_data: dict) -> DecisionTree:
        return DecisionTreeService.crear_desde_archivo(config_data)
