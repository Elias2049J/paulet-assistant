
from app.domain.entities.decision_tree.decision_node import DecisionNode


class DecisionTree:
    def __init__(self, root_node: 'DecisionNode'):
        self._root = root_node

    @property
    def root(self):
        return self._root
