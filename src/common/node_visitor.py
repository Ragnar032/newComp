# src/common/node_visitor.py

class NodeVisitor:
    def visit(self, node):
        method_name = f'visit_{node["tipo"]}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f"No se encontró un método visit_{node['tipo']}")