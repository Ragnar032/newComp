# src/optimizer/constant_folder.py
from src.common.node_visitor import NodeVisitor

class ConstantFolder(NodeVisitor):
    def optimize(self, ast):
        return self.visit(ast)

    def visit(self, node):
        if isinstance(node, dict) and 'tipo' in node:
            return super().visit(node)
        
        elif isinstance(node, list):
            return [self.visit(item) for item in node]
        
        elif isinstance(node, dict):
            new_node = {}
            for key, value in node.items():
                new_node[key] = self.visit(value)
            return new_node
            
        else:
            return node

    def generic_visit(self, node):
        if isinstance(node, dict):
            new_node = {}
            for key, value in node.items():
                if key != 'tipo':
                    new_node[key] = self.visit(value)
                else:
                    new_node[key] = value
            return new_node
        return node

    def visit_ExpresionBinaria(self, node):
        left = self.visit(node['izquierda'])
        right = self.visit(node['derecha'])

        if isinstance(left, dict) and isinstance(right, dict):
            if left.get('tipo') == 'LiteralNumerico' and right.get('tipo') == 'LiteralNumerico':
                try:
                    val_left = float(left['valor'])
                    val_right = float(right['valor'])
                    op = node['operador']
                    
                    result = None

                    if op == 'MAS':
                        result = val_left + val_right
                    elif op == 'MENOS':
                        result = val_left - val_right
                    elif op == 'POR':
                        result = val_left * val_right
                    elif op == 'DIV':
                        if val_right != 0:
                            result = val_left / val_right
                    
                    if result is not None:
                        if result.is_integer():
                            result = int(result)
                        return {'tipo': 'LiteralNumerico', 'valor': str(result)}
                except ValueError:
                    pass 

        return {
            'tipo': 'ExpresionBinaria', 
            'izquierda': left, 
            'operador': node['operador'], 
            'derecha': right
        }