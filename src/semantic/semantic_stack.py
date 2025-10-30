# src/semantic/semantic_stack.py (CORREGIDO)

from .variable_list import VariableList
from .semantic import SemanticError
from src.postfix_generator import PostfixGenerator
from .type_rules import TYPE_RULES

class SemanticStack:
    
    def __init__(self):
        self.variable_list = VariableList()
        self.postfix_gen = PostfixGenerator()
        self.type_rules = TYPE_RULES
        self.op_map_reverse = {
            '+': 'MAS', '-': 'MENOS', '*': 'POR', '/': 'DIV',
            '==': 'IGUALIGUAL', '<': 'MENOR', '>': 'MAYOR', 
            '<=': 'MENORIGUAL', '>=': 'MAYORIGUAL', '!=': 'DIFERENTE'
        }

    def analyze(self, ast):
        """Punto de entrada principal."""
        if ast:
            self.visit(ast)

    def visit(self, node):
        """Llama al método visitante específico."""
        method_name = f'visit_{node["tipo"]}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        """Visita genérica para nodos 'contenedores'."""
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
        
        if not self.variable_list.add_variable(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")

        postfix_string = self.postfix_gen.visit(node['valor'])
        expr_type = self._evaluate_postfix_type(postfix_string)
        
        if var_type != expr_type:
            if var_type == 'double' and expr_type == 'int':
                pass # Válido
            else:
                raise SemanticError(f"Error Semántico: No se puede asignar un valor de tipo '{expr_type}' a una variable de tipo '{var_type}'.")
    
    def visit_Asignacion(self, node):
        var_name = node['variable']
        variable = self.variable_list.find_variable(var_name)
        if not variable:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        
        postfix_string = self.postfix_gen.visit(node['valor'])
        expr_type = self._evaluate_postfix_type(postfix_string)
        
        if variable.tipo != expr_type:
            if variable.tipo == 'double' and expr_type == 'int':
                pass # Válido
            else:
                raise SemanticError(f"Error Semántico: Asignación inválida. Variable '{var_name}' es '{variable.tipo}' pero la expresión es '{expr_type}'.")

    def visit_LlamadaPrint(self, node):
        postfix_string = self.postfix_gen.visit(node['expresion'])
        self._evaluate_postfix_type(postfix_string)
        self.generic_visit(node)
    
    def visit_DeclaracionIf(self, node):
        postfix_string = self.postfix_gen.visit(node['condicion'])
        cond_type = self._evaluate_postfix_type(postfix_string)
        
        if cond_type != 'boolean':
            raise SemanticError(f"Error Semántico: La condición del IF debe ser booleana, pero se encontró '{cond_type}'.")
            
        for statement in node['cuerpo_if']:
            self.visit(statement)
            
        if node['cuerpo_else']:
            for statement in node['cuerpo_else']:
                self.visit(statement)
            
    def visit_DeclaracionWhile(self, node):
        postfix_string = self.postfix_gen.visit(node['condicion'])
        cond_type = self._evaluate_postfix_type(postfix_string)
        
        if cond_type != 'boolean':
            raise SemanticError(f"Error Semántico: La condición del WHILE debe ser booleana, pero se encontró '{cond_type}'.")
        
        for statement in node['cuerpo']:
            self.visit(statement)

    def _evaluate_postfix_type(self, postfix_string):
        """Implementación de la Pila 3 (Evaluación de Tipos)."""
        stack = []
        tokens = postfix_string.split()
        
        for token in tokens:
            if token in self.op_map_reverse:
                if len(stack) < 2:
                    raise SemanticError("Error Semántico: Expresión malformada (faltan operandos)")
                
                t2 = stack.pop()
                t1 = stack.pop()
                op_rule = self.op_map_reverse[token]
                result_type = self.type_rules.get(op_rule, {}).get(t1, {}).get(t2, 'error')
                
                if result_type == 'error':
                    raise SemanticError(f"Error Semántico: Operación inválida. No se puede aplicar '{token}' a los tipos '{t1}' y '{t2}'.")
                
                stack.append(result_type)
                
            else:
                if token.startswith('"') and token.endswith('"'):
                    stack.append('String')
                elif token == 'true' or token == 'false':
                    stack.append('boolean')
                elif token.replace('.', '', 1).isdigit():
                    stack.append('double' if '.' in token else 'int')
                else:
                    variable = self.variable_list.find_variable(token)
                    if not variable:
                        raise SemanticError(f"Error Semántico: Variable '{token}' no declarada.")
                    stack.append(variable.tipo)
        
        if len(stack) != 1:
            raise SemanticError("Error Semántico: Expresión malformada.")
            
        return stack.pop()