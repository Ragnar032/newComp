# src/semantic/semantic.py

from .semantic_stack import SemanticStack
from .semantic_error import SemanticError  

class Semantic:
    def __init__(self):
        self.expert = SemanticStack()

    def analyze(self, ast):
        return self.expert.analyze(ast)