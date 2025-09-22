# semantic_analyzer.py
from symbol_table import SymbolTable

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
    
        self.type_rules = {
            'MAS': {
                'int': {'int': 'int', 'double': 'double', 'String': 'error', 'boolean': 'error'},
                'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
            },
            'MENOS': {
                'int': {'int': 'int', 'double': 'double', 'String': 'error', 'boolean': 'error'},
                'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
            },
            'POR': {
                'int': {'int': 'int', 'double': 'double', 'String': 'error', 'boolean': 'error'},
                'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
            },
            'DIV': {
                
                'int': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
                'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
            },
            'IGUALIGUAL': {
                'int': {'int': 'boolean', 'double': 'boolean', 'String': 'error', 'boolean': 'error'},
                'double': {'int': 'boolean', 'double': 'boolean', 'String': 'error', 'boolean': 'error'},
                'String': {'String': 'boolean'}, 
                'boolean': {'boolean': 'boolean'},
            },
        }

    def visit(self, node):
        """
        Este es el método "director" o "despachador".
        Lee el 'tipo' del nodo del AST (ej. 'DeclaracionVariable') y llama a la función
        visit_... correspondiente (ej. 'visit_DeclaracionVariable').
        """
        method_name = f'visit_{node["tipo"]}'
        # getattr busca un método en esta clase con el nombre que construimos.
        # Si no lo encuentra, usa 'generic_visit' como plan B.
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """
        Un visitador genérico que simplemente avanza el recorrido del árbol
        hacia los nodos hijos, en caso de que un nodo no tenga un método 'visit_' específico.
        """
        for key, value in node.items():
            if isinstance(value, dict):
                self.visit(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.visit(item)

    def analyze(self, ast):
        """Punto de entrada principal. Inicia el recorrido del AST desde la raíz."""
        if ast:
            self.visit(ast)

    # --- Métodos Visitantes para Nodos Específicos del AST ---

    def visit_DeclaracionVariable(self, node):
        """
        Se llama cuando se encuentra un nodo de declaración de variable en el AST.
        Aquí se validan las variables duplicadas y la asignación de tipos.
        """
        var_name = node['nombre']
        var_type = node['tipo_dato']
        
        # REGLA 1: DETECCIÓN DE VARIABLE DUPLICADA
        if not self.symbol_table.define(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")

        expr_type = self.visit(node['valor'])
        
        # REGLA 3: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS (en asignación)
    
        if var_type != expr_type:
            raise SemanticError(f"Error Semántico: No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")

    def visit_Variable(self, node):
        """
        Se llama cuando se encuentra un nodo de uso de variable (ej. en el lado derecho de una expresión).
        Aquí se validan las variables no declaradas.
        """
        var_name = node['nombre']
        
        symbol = self.symbol_table.lookup(var_name)
        if not symbol:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        
        return symbol.type

    def visit_ExpresionBinaria(self, node):
        """
        Se llama para un nodo de operación binaria (ej. 5 + x).
        Aquí se valida la compatibilidad de tipos en las operaciones.
        """
        left_type = self.visit(node['izquierda'])
        right_type = self.visit(node['derecha'])
        op = node['operador']
        

        result_type = self.type_rules.get(op, {}).get(left_type, {}).get(right_type, 'error')
        
        if result_type == 'error':
            raise SemanticError(f"Error Semántico: Operación inválida. No se puede aplicar el operador '{op}' a los tipos '{left_type}' y '{right_type}'.")
            
        return result_type

    def visit_LiteralNumerico(self, node):
        """Determina si un número en el AST es 'int' o 'double'."""
        if '.' in node['valor']:
            return 'double'
        return 'int'