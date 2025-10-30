# src/postfix_visitor.py

from src.postfix_generator import PostfixGenerator 

class FullPostfixVisitor:
    
    def __init__(self):
        self.postfix_gen = PostfixGenerator()
        self.label_counter = 0

    def _new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter - 1}"

    def visit(self, node):
        method_name = f'visit_{node["tipo"]}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        return None

    def visit_DeclaracionClase(self, node):
        print(f"CLASS: {node['nombre']}")
        print("="*30)
        for member in node['cuerpo']:
            self.visit(member)
        print("="*30)
        return None

    def visit_DeclaracionMetodo(self, node):
        print(f"\nMETHOD: {node['nombre']}():")
        print("---")
        for statement in node['cuerpo']:
            postfix_instruction = self.visit(statement)
            if postfix_instruction:
                print(postfix_instruction)
        return None

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
            body_if_str += f"\n\t{self.visit(stmt)}"
        
        if node['cuerpo_else']:
            body_else_str = ""
            for stmt in node['cuerpo_else']:
                body_else_str += f"\n\t{self.visit(stmt)}"
            
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
            body_str += f"\n\t{self.visit(stmt)}"
        
        return (
            f"{label_inicio}:\n"
            f"\t{cond_postfix} {label_fin} JUMP_IF_FALSE"
            f"{body_str}\n"
            f"\t{label_inicio} GOTO\n"
            f"{label_fin}:"
        )