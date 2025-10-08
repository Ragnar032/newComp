# src/semantic/semantic.py

from .variable_list import VariableList

class SemanticError(Exception):
    pass

class Semantic:
    def __init__(self):
        self.variable_list = VariableList()
        
        # Reglas de compatibilidad de tipos para operaciones binarias
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
            'MENORIGUAL': {
                'int': {'int': 'boolean', 'double': 'boolean'},
                'double': {'int': 'boolean', 'double': 'boolean'},
            },
            'MAYORIGUAL': {
                'int': {'int': 'boolean', 'double': 'boolean'},
                'double': {'int': 'boolean', 'double': 'boolean'},
            },
            'MENORQUE': { 
                'int': {'int': 'boolean', 'double': 'boolean'},
                'double': {'int': 'boolean', 'double': 'boolean'},
            },
            'MAYORQUE': { 
                'int': {'int': 'boolean', 'double': 'boolean'},
                'double': {'int': 'boolean', 'double': 'boolean'},
            }
        }

    def analyze(self, ast):
        if ast:
            self.visit(ast)

    def visit(self, node):
        method_name = f'visit_{node["tipo"]}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for key, value in node.items():
            if isinstance(value, dict):
                self.visit(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.visit(item)

    def visit_DeclaracionVariable(self, node):
        var_name = node['nombre']
        var_type = node['tipo_dato']
        
        # REGLA 1: DETECCIÓN DE VARIABLE DUPLICADA
        if not self.variable_list.add_variable(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")

        # Visita la expresión del lado derecho para obtener su tipo resultante
        expr_type = self.visit(node['valor'])
        
        # REGLA 2: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS EN ASIGNACIÓN
        if var_type != expr_type:
            # Una excepción común: permitir asignar un int a un double
            if var_type == 'double' and expr_type == 'int':
                pass # Esto es válido
            else:
                raise SemanticError(f"Error Semántico: No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")

    def visit_Variable(self, node):
        var_name = node['nombre']
        
        # REGLA 3: DETECCIÓN DE VARIABLE NO DECLARADA
        variable = self.variable_list.find_variable(var_name)
        if not variable:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        
        return variable.tipo

    def visit_ExpresionBinaria(self, node):

        left_type = self.visit(node['izquierda'])
        right_type = self.visit(node['derecha'])
        op = node['operador']
        
        # REGLA 4: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS EN OPERACIONES
        result_type = self.type_rules.get(op, {}).get(left_type, {}).get(right_type, 'error')
        
        if result_type == 'error':
            raise SemanticError(f"Error Semántico: Operación inválida. No se puede aplicar el operador '{op}' a los tipos '{left_type}' y '{right_type}'.")
            
        return result_type

    def visit_LiteralNumerico(self, node):
        if '.' in str(node['valor']):
            return 'double'
        return 'int'

    def visit_LiteralCadena(self, node):
        return 'String'

    def visit_LiteralBooleano(self, node):
        return 'boolean'