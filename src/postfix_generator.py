# src/postfix_generator.py

class PostfixGenerator:
    def __init__(self):
        self.op_map = {
            'MAS': '+',
            'MENOS': '-',
            'POR': '*',
            'DIV': '/',
            'IGUALIGUAL': '==',
            'DIFERENTE': '!=',
            'MENOR': '<',
            'MENORIGUAL': '<=',
            'MAYOR': '>',
            'MAYORIGUAL': '>='
        }

    def visit(self, node):
        method_name = f'visit_{node["tipo"]}'
        visitor = getattr(self, method_name, self.unsupported_node)
        return visitor(node)

    def unsupported_node(self, node):
        raise Exception(f"Error de Postfix: No se puede procesar el tipo de nodo '{node.get('tipo')}'")


    def visit_ExpresionBinaria(self, node):

        
        left_str = self.visit(node['izquierda'])
        
        right_str = self.visit(node['derecha'])
        
        op_str = self.op_map.get(node['operador'])
        if op_str is None:
             raise Exception(f"Error de Postfix: Operador desconocido '{node['operador']}'")
        
        return f"{left_str} {right_str} {op_str}"

    def visit_LiteralNumerico(self, node):
        return str(node['valor'])

    def visit_Variable(self, node):
        return str(node['nombre'])

    def visit_LiteralCadena(self, node):
        return f'"{node["valor"]}"'
        
    def visit_LiteralBooleano(self, node):
        return str(node['valor']).lower()