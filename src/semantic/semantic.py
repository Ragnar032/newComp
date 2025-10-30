# src/semantic/semantic.py

from .variable_list import VariableList

class SemanticError(Exception):
    pass

class Semantic:
    def __init__(self):
        self.variable_list = VariableList()
        
        # ... (Aquí irían tus type_rules, que movimos)
        # ... self.type_rules = ...

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
        
        # -----------------------------------------------------------------
        # ALGORITMO 1: DETECCIÓN DE VARIABLE DUPLICADA
        # -----------------------------------------------------------------
        # 1. Se intenta añadir la variable (nombre y tipo) a la lista de variables.
        # 2. El método `add_variable` comprueba internamente 
        #    si el nombre (`var_name`) ya existe en su diccionario (`self.variables`)
        #   .
        # 3. Si ya existe, `add_variable` devuelve `False`.
        # 4. Este `if` detecta ese `False` y lanza el error semántico indicando
        #    que la variable ya fue declarada.
        if not self.variable_list.add_variable(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")
        # -----------------------------------------------------------------

        # Visita la expresión del lado derecho para obtener su tipo resultante
        expr_type = self.visit(node['valor'])
        
        # -----------------------------------------------------------------
        # ALGORITMO 2: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS EN ASIGNACIÓN
        # -----------------------------------------------------------------
        # 1. Compara el tipo declarado de la variable (`var_type`, ej: 'double')
        #    con el tipo resultante de la expresión (`expr_type`, ej: 'int').
        if var_type != expr_type:
            
            # 2. Se define una excepción (casting implícito):
            #    Permitir que un 'int' se asigne a un 'double' es válido.
            if var_type == 'double' and expr_type == 'int':
                pass # Esto es válido
            else:
                # 3. Si los tipos no coinciden Y no es la excepción permitida,
                #    se lanza un error de incompatibilidad de tipos.
                raise SemanticError(f"Error Semántico: No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
        # -----------------------------------------------------------------

    def visit_Variable(self, node):
        var_name = node['nombre']
        
        # -----------------------------------------------------------------
        # ALGORITMO 3: DETECCIÓN DE VARIABLE NO DECLARADA
        # -----------------------------------------------------------------
        # 1. Este método se llama cada vez que se *usa* una variable 
        #    (ej. en el lado derecho de una asignación o en un 'print').
        # 2. Se intenta buscar la variable (`var_name`) en la lista de variables.
        variable = self.variable_list.find_variable(var_name)
        
        # 3. El método `find_variable` devuelve `None` (o 'nada') si la
        #    variable no se encuentra en su diccionario.
        # 4. Este `if` detecta si el resultado es `None` (not variable) y
        #    lanza el error, indicando que la variable no ha sido declarada.
        if not variable:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        # -----------------------------------------------------------------
        
        # Si la variable SÍ se encontró, devuelve su tipo (ej: 'int')
        # para que pueda ser usado en la evaluación de la expresión.
        return variable.tipo

    def visit_ExpresionBinaria(self, node):
        # Este método visita recursivamente el árbol de expresiones
        # para encontrar el tipo final.
        left_type = self.visit(node['izquierda'])
        right_type = self.visit(node['derecha'])
        op = node['operador']
        
        # REGLA 4: DETECCIÓN DE INCOMPATIBILIDAD DE TIPOS EN OPERACIONES
        # (Esto es similar al Algoritmo 2, pero para operadores como +, -, *, /)
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