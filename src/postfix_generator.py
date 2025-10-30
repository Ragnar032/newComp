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
        """Maneja nodos que no son parte de una expresión."""
        # Esto no debería pasar si se llama correctamente
        # desde ICG_Generator o SemanticStack.
        raise Exception(f"Error de Postfix: No se puede procesar el tipo de nodo '{node.get('tipo')}'")


    def visit_ExpresionBinaria(self, node):

        # 1. Visita Izquierda (devuelve string)
        left_str = self.visit(node['izquierda'])
        
        # 2. Visita Derecha (devuelve string)
        right_str = self.visit(node['derecha'])
        
        # 3. Obtiene el operador del mapa
        op_str = self.op_map.get(node['operador'])
        if op_str is None:
             raise Exception(f"Error de Postfix: Operador desconocido '{node['operador']}'")
        
        # 4. Devuelve el string combinado
        return f"{left_str} {right_str} {op_str}"

    def visit_LiteralNumerico(self, node):
        """Devuelve el valor literal como string."""
        return str(node['valor'])

    def visit_Variable(self, node):
        """Devuelve el nombre de la variable."""
        return str(node['nombre'])

    def visit_LiteralCadena(self, node):
        """Devuelve la cadena literal (con comillas)."""
        return f'"{node["valor"]}"'
        
    def visit_LiteralBooleano(self, node):
        """Devuelve el booleano literal."""
        # Asegurarse que esté en minúsculas
        return str(node['valor']).lower()