# src/semantic/semantic_stack.py
from .variable_list import VariableList
from .semantic_error import SemanticError
from src.postfix_generator import PostfixGenerator
from .type_rules import TYPE_RULES
from src.common.constants import OperatorMap
from src.common.node_visitor import NodeVisitor

class SemanticStack(NodeVisitor):
    
    def __init__(self):
        self.variable_list = VariableList()
        self.postfix_gen = PostfixGenerator()
        self.type_rules = TYPE_RULES
        self.op_map_reverse = OperatorMap.REVERSE_MAP

    def analyze(self, ast):
        if ast:
            self.visit(ast)
    
    def generic_visit(self, node):
        for key, value in node.items():
            if isinstance(value, dict):
                self.visit(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self.visit(item)

    # --- NUEVA FUNCIÓN: TOKENIZADOR INTELIGENTE ---
    def _smart_split(self, text):
        """
        Divide el texto por espacios, PERO respeta lo que esté entre comillas.
        Ejemplo: 'print "Hola Mundo"' -> ['print', '"Hola Mundo"']
        """
        tokens = []
        token_actual = ""
        dentro_comillas = False
        
        for char in text:
            if char == '"':
                dentro_comillas = not dentro_comillas # Entramos o salimos de comillas
                token_actual += char
            elif char == ' ' and not dentro_comillas:
                # Si encontramos un espacio y NO estamos en comillas, cortamos el token
                if token_actual:
                    tokens.append(token_actual)
                    token_actual = ""
            else:
                token_actual += char
        
        if token_actual:
            tokens.append(token_actual)
            
        return tokens
    # -----------------------------------------------

    def _check_assignment_compatibility(self, var_type, expr_type):
        if var_type == expr_type:
            return True
        if var_type == 'double' and expr_type == 'int':
            return True
        return False

    def _verify_condition(self, condition_node, context_name):
        postfix_string = self.postfix_gen.visit(condition_node)
        cond_type = self._evaluate_postfix_type(postfix_string)
        
        if cond_type != 'boolean':
            raise SemanticError(f"Error Semántico: La condición del {context_name} debe ser booleana, pero se encontró '{cond_type}'.")

    def visit_DeclaracionVariable(self, node):
        var_name = node['nombre']
        var_type = node['tipo_dato']
        
        if not self.variable_list.add_variable(var_name, var_type):
            raise SemanticError(f"Error Semántico: La variable '{var_name}' ya ha sido declarada.")

        postfix_string = self.postfix_gen.visit(node['valor'])
        expr_type = self._evaluate_postfix_type(postfix_string)
        
        if not self._check_assignment_compatibility(var_type, expr_type):
            raise SemanticError(f"Error Semántico: Asignación inválida. Variable '{var_name}' es '{var_type}' pero la expresión es '{expr_type}'.")
   
    def visit_Asignacion(self, node):
        var_name = node['variable']
        variable = self.variable_list.find_variable(var_name)
        if not variable:
            raise SemanticError(f"Error Semántico: La variable '{var_name}' no ha sido declarada.")
        
        postfix_string = self.postfix_gen.visit(node['valor'])
        expr_type = self._evaluate_postfix_type(postfix_string)
        
        if not self._check_assignment_compatibility(variable.tipo, expr_type):
            raise SemanticError(f"Error Semántico: Asignación inválida. Variable '{var_name}' es '{variable.tipo}' pero la expresión es '{expr_type}'.")

    def visit_LlamadaPrint(self, node):
        postfix_string = self.postfix_gen.visit(node['expresion'])
        self._evaluate_postfix_type(postfix_string)
        # No llamamos a generic_visit aquí para evitar recursión innecesaria en la expresión ya visitada
    
    def visit_DeclaracionIf(self, node):
        self._verify_condition(node['condicion'], "IF")
        for statement in node['cuerpo_if']:
            self.visit(statement)
        if node['cuerpo_else']:
            for statement in node['cuerpo_else']:
                self.visit(statement)
            
    def visit_DeclaracionWhile(self, node):
        self._verify_condition(node['condicion'], "WHILE")
        for statement in node['cuerpo']:
            self.visit(statement)

    def _evaluate_postfix_type(self, postfix_string):
        stack = []
        
        # --- AQUÍ USAMOS EL NUEVO MÉTODO EN VEZ DE .split() ---
        tokens = self._smart_split(postfix_string)
        # ------------------------------------------------------
        
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
                # Ahora token será '"Es Mayor"' completo, así que entrará en este IF correctamente
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