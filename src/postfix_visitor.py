# src/postfix_visitor.py
from src.postfix_generator import PostfixGenerator 
from src.common.node_visitor import NodeVisitor

class FullPostfixVisitor(NodeVisitor):
    
    def __init__(self):
        self.postfix_gen = PostfixGenerator()
        self.label_counter = 0

    def _new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter - 1}"
    
    def generic_visit(self, node):
        return "" # Importante: devuelve cadena vacía en lugar de None

    def visit_DeclaracionClase(self, node):
        # Acumulamos todo el código de los métodos en esta variable
        full_code = ""
        for member in node['cuerpo']:
            res = self.visit(member)
            if res:
                full_code += res + "\n"
        return full_code

    def visit_DeclaracionMetodo(self, node):
        # Acumulamos las instrucciones del método
        method_code = ""
        for statement in node['cuerpo']:
            stmt_code = self.visit(statement)
            if stmt_code:
                method_code += stmt_code + "\n"
        return method_code

    def visit_DeclaracionVariable(self, node):
        var_name = node['nombre']
        expr_postfix = self.postfix_gen.visit(node['valor'])
        return f"{var_name} {expr_postfix} ="

    def visit_Asignacion(self, node):
        var_name = node['variable']
        expr_postfix = self.postfix_gen.visit(node['valor'])
        return f"{var_name} {expr_postfix} ="

    def visit_LlamadaPrint(self, node):
        expr_postfix = self.postfix_gen.visit(node['expresion'])
        return f"{expr_postfix} PRINT"
        
    def visit_DeclaracionIf(self, node):
        label_else = self._new_label()
        label_fin = self._new_label()
        cond_postfix = self.postfix_gen.visit(node['condicion'])
        
        body_if_str = ""
        for stmt in node['cuerpo_if']:
            res = self.visit(stmt)
            if res: body_if_str += f"\n\t{res}"
        
        if node['cuerpo_else']:
            body_else_str = ""
            for stmt in node['cuerpo_else']:
                res = self.visit(stmt)
                if res: body_else_str += f"\n\t{res}"
            
            return (
                f"{cond_postfix} {label_else} JUMP_IF_FALSE"
                f"{body_if_str}\n"
                f"{label_fin} GOTO\n"
                f"{label_else}:"
                f"{body_else_str}\n"
                f"{label_fin}:"
            )
        else:
            return (
                f"{cond_postfix} {label_fin} JUMP_IF_FALSE"
                f"{body_if_str}\n"
                f"{label_fin}:"
            )
            
    def visit_DeclaracionWhile(self, node):
        label_inicio = self._new_label()
        label_fin = self._new_label()
        cond_postfix = self.postfix_gen.visit(node['condicion'])
        
        body_str = ""
        for stmt in node['cuerpo']:
            res = self.visit(stmt)
            if res: body_str += f"\n\t{res}"
        
        return (
            f"{label_inicio}:\n"
            f"\t{cond_postfix} {label_fin} JUMP_IF_FALSE"
            f"{body_str}\n"
            f"\t{label_inicio} GOTO\n"
            f"{label_fin}:"
        )