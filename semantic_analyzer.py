# semantic_analyzer.py

from variable_list import VariableList

class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        # CAMBIO 2: Crear una instancia de 'VariableList'
        self.variable_list = VariableList()
        
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
        method_name = f'visit_{node["tipo"]}'
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

    def visit_DeclaracionVariable(self, node):
        """
        Se llama cuando se encuentra un nodo de declaración de variable en el AST.
        Aquí se validan las variables duplicadas y la asignación de tipos.
        """
        var_name = node['nombre']
        var_type = node['tipo_dato']
        
        # REGLA 1: DETECCIÓN DE VARIABLE DUPLICADA
        # CAMBIO 3: Usar el método 'add_variable' del objeto 'variable_list'
        if not self.variable_list.add_variable(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")

        expr_type = self.visit(node['valor'])
        
        # REGLA 3: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS
        if var_type != expr_type:
            raise SemanticError(f"Error Semántico: No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")

    def visit_Variable(self, node):
        """
        Se llama cuando se encuentra un nodo de uso de variable (ej. en el lado derecho de una expresión).
        Aquí se validan las variables no declaradas.
        """
        var_name = node['nombre']
        
        # REGLA 2: DETECCIÓN DE VARIABLE NO DECLARADA
        # CAMBIO 4: Usar el método 'find_variable' y guardar el resultado en 'variable'
        variable = self.variable_list.find_variable(var_name)
        if not variable:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        
        # CAMBIO 5: Acceder al atributo '.tipo' del objeto 'Variable'
        return variable.tipo

    def visit_ExpresionBinaria(self, node):
        """
        Se llama para un nodo de operación binaria (ej. 5 + x).
        Aquí se valida la compatibilidad de tipos en las operaciones.
        """
        left_type = self.visit(node['izquierda'])
        right_type = self.visit(node['derecha'])
        op = node['operador']
        
        # REGLA 3: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS en operaciones
        result_type = self.type_rules.get(op, {}).get(left_type, {}).get(right_type, 'error')
        
        if result_type == 'error':
            raise SemanticError(f"Error Semántico: Operación inválida. No se puede aplicar el operador '{op}' a los tipos '{left_type}' y '{right_type}'.")
            
        return result_type

    def visit_LiteralNumerico(self, node):
        """Determina si un número en el AST es 'int' o 'double'."""
        if '.' in node['valor']:
            return 'double'
        return 'int'