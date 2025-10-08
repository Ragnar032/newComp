# src/parser/grammar_rules.py

from .parser_auxiliaries import ParserAuxiliaries, ParsingError

class GrammarRules(ParserAuxiliaries):
    """
    Capa intermedia que define las reglas de la gramática.
    Hereda la gestión de tokens de ParserAuxiliaries.
    """

    def parse_class_declaration(self):
        self.eat('PUBLIC')
        self.eat('CLASS')
        class_name = self.current_token['valor']
        self.eat('ID')
        self.eat('LLAVE_IZQ')
        
        class_body = []
        while self.current_token['tipo'] != 'LLAVE_DER' and self.current_token['tipo'] != 'EOF':
            class_body.append(self.parse_member_declaration())

        self.eat('LLAVE_DER')
        
        return {'tipo': 'DeclaracionClase', 'nombre': class_name, 'cuerpo': class_body}

    # ... TODOS los demás métodos parse_* van aquí sin cambios ...
    # (parse_member_declaration, parse_expression, parse_term, etc.)
    def parse_member_declaration(self):
        if self.current_token['tipo'] in ['PUBLIC', 'PRIVATE']:
            return self.parse_method_declaration()
        
        data_types = ['INT', 'DOUBLE', 'BOOLEAN', 'STRINGTYPE']
        if self.current_token['tipo'] in data_types:
            return self.parse_variable_declaration()
        
        raise ParsingError(f"Declaración inesperada dentro de la clase, no se puede empezar con '{self.current_token['tipo']}'")

    def parse_method_declaration(self):
        self.eat('PUBLIC')
        
        if self.current_token['tipo'] == 'STATIC':
            return self.parse_main_method_declaration()
        else:
            return self.parse_generic_method_declaration()

    def parse_main_method_declaration(self):
        self.eat('STATIC')
        self.eat('VOID')
        self.eat('MAIN')
        self.eat('PARENTESIS_IZQ')
        self.eat('STRINGTYPE')
        self.eat('CORCHETE_IZQ')
        self.eat('CORCHETE_DER')
        self.eat('ID')
        self.eat('PARENTESIS_DER')
        
        method_body = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionMetodo', 'nombre': 'main', 'tipo_retorno': 'void', 'cuerpo': method_body}

    def parse_generic_method_declaration(self):
        return_type = self.current_token['valor']
        self.advance()
        
        method_name = self.current_token['valor']
        self.eat('ID')
        
        self.eat('PARENTESIS_IZQ')
        self.eat('PARENTESIS_DER')
        
        method_body = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionMetodo', 'nombre': method_name, 'tipo_retorno': return_type, 'cuerpo': method_body}

    def parse_block_statement(self):
        self.eat('LLAVE_IZQ')
        statements = []
        while self.current_token['tipo'] != 'LLAVE_DER' and self.current_token['tipo'] != 'EOF':
            statements.append(self.parse_statement())
        self.eat('LLAVE_DER')
        return statements

    def parse_statement(self):
        data_types = ['INT', 'DOUBLE', 'BOOLEAN', 'STRINGTYPE']
        if self.current_token['tipo'] in data_types:
            return self.parse_variable_declaration()
        elif self.current_token['tipo'] == 'PRINT':
            return self.parse_print_statement()
        elif self.current_token['tipo'] == 'ID' and self.tokens[self.pos + 1]['tipo'] == 'PARENTESIS_IZQ':
            return self.parse_function_call()
        else:
            raise ParsingError(f"Sentencia no reconocida, no puede empezar con '{self.current_token['tipo']}'")
            
    def parse_print_statement(self):
        self.eat('PRINT')
        self.eat('PARENTESIS_IZQ')
        expression = self.parse_expression()
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaPrint', 'expresion': expression}
    
    def parse_function_call(self):
        function_name = self.current_token['valor']
        self.eat('ID')
        self.eat('PARENTESIS_IZQ')
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaFuncion', 'nombre': function_name}

    def parse_variable_declaration(self):
        data_type = self.current_token
        self.advance()
        variable_name = self.current_token
        self.eat('ID')
        self.eat('IGUAL')
        value = self.parse_expression()
        self.eat('PUNTOCOMA')
        return {'tipo': 'DeclaracionVariable', 'tipo_dato': data_type['valor'], 'nombre': variable_name['valor'], 'valor': value}

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token['tipo'] in ['MAS', 'MENOS']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_term()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token['tipo'] in ['POR', 'DIV']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_factor()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_factor(self):
        token = self.current_token
        if token['tipo'] == 'NUMBER':
            self.eat('NUMBER')
            return {'tipo': 'LiteralNumerico', 'valor': token['valor']}
        elif token['tipo'] == 'ID':
            self.eat('ID')
            return {'tipo': 'Variable', 'nombre': token['valor']}
        elif token['tipo'] == 'CADENA':
            self.eat('CADENA')
            return {'tipo': 'LiteralCadena', 'valor': token['valor']}
        elif token['tipo'] == 'PARENTESIS_IZQ':
            self.eat('PARENTESIS_IZQ')
            node = self.parse_expression()
            self.eat('PARENTESIS_DER')
            return node
        else:
            raise ParsingError(f"Factor inesperado, no se puede empezar con '{token['tipo']}'")