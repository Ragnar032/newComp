# src/intermediate/quadruple_generator.py
from src.common.node_visitor import NodeVisitor

class QuadrupleGenerator(NodeVisitor):
    def __init__(self):
        self.quadruples = []
        self.temp_counter = 0
        self.label_counter = 0

    def _new_temp(self):
        self.temp_counter += 1
        return f"T{self.temp_counter}"

    def _new_label(self):
        self.label_counter += 1
        return f"L{self.label_counter}"

    def generate(self, node):
        self.quadruples = []
        self.temp_counter = 0
        self.label_counter = 0
        self.visit(node)
        return self.quadruples

    def generic_visit(self, node):
        if isinstance(node, list):
            for item in node:
                self.visit(item)
        elif isinstance(node, dict):
            pass

    # --- ESTRUCTURA ---
    def visit_DeclaracionClase(self, node):
        for member in node['cuerpo']:
            self.visit(member)

    def visit_DeclaracionMetodo(self, node):
        for statement in node['cuerpo']:
            self.visit(statement)

    # --- EXPRESIONES (Retornan temporal o valor) ---
    def visit_ExpresionBinaria(self, node):
        arg1 = self.visit(node['izquierda'])
        arg2 = self.visit(node['derecha'])
        result = self._new_temp()
        
        # Mapeo de operadores
        op_map = {
            'MAS': '+', 'MENOS': '-', 'POR': '*', 'DIV': '/',
            'IGUALIGUAL': '==', 'DIFERENTE': '!=',
            'MAYOR': '>', 'MENOR': '<', 
            'MAYORIGUAL': '>=', 'MENORIGUAL': '<='
        }
        op = op_map.get(node['operador'], node['operador'])

        self.quadruples.append({'op': op, 'arg1': arg1, 'arg2': arg2, 'res': result})
        return result

    def visit_LiteralNumerico(self, node):
        return str(node['valor'])

    def visit_LiteralCadena(self, node):
        return f'"{node["valor"]}"'
    
    def visit_LiteralBooleano(self, node):
        return "1" if node['valor'] == 'true' else "0"
    
    def visit_Variable(self, node):
        return node['nombre']

    # --- SENTENCIAS (Generan quads, no retornan) ---
    def visit_DeclaracionVariable(self, node):
        val_address = self.visit(node['valor'])
        self.quadruples.append({'op': '=', 'arg1': val_address, 'arg2': None, 'res': node['nombre']})

    def visit_Asignacion(self, node):
        val_address = self.visit(node['valor'])
        self.quadruples.append({'op': '=', 'arg1': val_address, 'arg2': None, 'res': node['variable']})

    def visit_LlamadaPrint(self, node):
        val_address = self.visit(node['expresion'])
        self.quadruples.append({'op': 'PRINT', 'arg1': val_address, 'arg2': None, 'res': None})

    def visit_DeclaracionIf(self, node):
        label_else = self._new_label()
        label_end = self._new_label()

        cond_res = self.visit(node['condicion'])
        
        # Salto si Falso
        target = label_else if node['cuerpo_else'] else label_end
        self.quadruples.append({'op': 'JUMP_IF_FALSE', 'arg1': cond_res, 'arg2': None, 'res': target})

        # Cuerpo True
        for stmt in node['cuerpo_if']:
            self.visit(stmt)

        # Cuerpo False (si existe)
        if node['cuerpo_else']:
            self.quadruples.append({'op': 'GOTO', 'arg1': None, 'arg2': None, 'res': label_end})
            self.quadruples.append({'op': 'LABEL', 'arg1': None, 'arg2': None, 'res': label_else})
            for stmt in node['cuerpo_else']:
                self.visit(stmt)
            self.quadruples.append({'op': 'LABEL', 'arg1': None, 'arg2': None, 'res': label_end})
        else:
            self.quadruples.append({'op': 'LABEL', 'arg1': None, 'arg2': None, 'res': label_end})

    def visit_DeclaracionWhile(self, node):
        label_start = self._new_label()
        label_end = self._new_label()

        self.quadruples.append({'op': 'LABEL', 'arg1': None, 'arg2': None, 'res': label_start})
        cond_res = self.visit(node['condicion'])
        
        self.quadruples.append({'op': 'JUMP_IF_FALSE', 'arg1': cond_res, 'arg2': None, 'res': label_end})
        
        for stmt in node['cuerpo']:
            self.visit(stmt)
            
        self.quadruples.append({'op': 'GOTO', 'arg1': None, 'arg2': None, 'res': label_start})
        self.quadruples.append({'op': 'LABEL', 'arg1': None, 'arg2': None, 'res': label_end})