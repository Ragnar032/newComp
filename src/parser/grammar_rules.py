# src/parser/grammar_rules.py

from .parser_auxiliaries import ParserAuxiliaries, ParsingError

class GrammarRules(ParserAuxiliaries):
    def parse_class_declaration(self):
        """
        BNF: <class_declaration> ::= PUBLIC CLASS ID '{' (<member_declaration>)* '}'
        """
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

    def parse_member_declaration(self):
        """
        BNF: <member_declaration> ::= <method_declaration> | <variable_declaration>
        """
        if self.current_token['tipo'] in ['PUBLIC', 'PRIVATE']:
            return self.parse_method_declaration()
        
        data_types = ['INT', 'DOUBLE', 'BOOLEAN', 'STRINGTYPE']
        if self.current_token['tipo'] in data_types:
            return self.parse_variable_declaration()
        
        raise ParsingError(f"Declaración inesperada dentro de la clase, no se puede empezar con '{self.current_token['tipo']}'")

    def parse_method_declaration(self):
        """Dispatcher para los diferentes tipos de métodos."""
        self.eat('PUBLIC')
        
        if self.current_token['tipo'] == 'STATIC':
            return self.parse_main_method_declaration()
        else:
            return self.parse_generic_method_declaration()

    def parse_main_method_declaration(self):
        """
        BNF: <main_method> ::= STATIC VOID MAIN '(' STRINGTYPE '[' ']' ID ')' <block_statement>
        """
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
        """
        BNF: <generic_method> ::= <type> ID '(' ')' <block_statement>
        """
        return_type = self.current_token['valor']
        self.advance()
        
        method_name = self.current_token['valor']
        self.eat('ID')
        
        self.eat('PARENTESIS_IZQ')
        self.eat('PARENTESIS_DER')
        
        method_body = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionMetodo', 'nombre': method_name, 'tipo_retorno': return_type, 'cuerpo': method_body}

    def parse_block_statement(self):
        """
        BNF: <block_statement> ::= '{' (<statement>)* '}'
        """
        self.eat('LLAVE_IZQ')
        statements = []
        while self.current_token['tipo'] != 'LLAVE_DER' and self.current_token['tipo'] != 'EOF':
            statements.append(self.parse_statement())
        self.eat('LLAVE_DER')
        return statements

    def parse_statement(self):
        """
        BNF: <statement> ::= <variable_declaration> | <assignment_statement> | <print_statement> | 
                             <if_statement> | <while_statement> | <for_statement> | <function_call>
        """
        token_type = self.current_token['tipo']
        
        data_types = ['INT', 'DOUBLE', 'BOOLEAN', 'STRINGTYPE']
        if token_type in data_types:
            return self.parse_variable_declaration()
        elif token_type == 'PRINT':
            return self.parse_print_statement()
        elif token_type == 'IF':
            return self.parse_if_statement()
        elif token_type == 'WHILE':
            return self.parse_while_statement()
        elif token_type == 'FOR':
            return self.parse_for_statement()
        elif token_type == 'ID' and self.peek()['tipo'] == 'IGUAL':
            return self.parse_assignment_statement()
        elif token_type == 'ID' and self.peek()['tipo'] == 'PARENTESIS_IZQ':
            return self.parse_function_call()
        else:
            raise ParsingError(f"Sentencia no reconocida, no puede empezar con '{token_type}'")
    
    def parse_while_statement(self):
        """
        BNF: <while_statement> ::= WHILE '(' <expression> ')' <block_statement>
        """
        self.eat('WHILE')
        self.eat('PARENTESIS_IZQ')
        condicion = self.parse_expression()
        self.eat('PARENTESIS_DER')
        
        cuerpo = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionWhile', 'condicion': condicion, 'cuerpo': cuerpo}
    
    def parse_for_statement(self):
        """
        BNF: <for_statement> ::= FOR '(' <variable_declaration_no_semicolon> ';' <expression> ';' <assignment_expression> ')' <block_statement>
        """
        self.eat('FOR')
        self.eat('PARENTESIS_IZQ')
        
        inicializador = self.parse_variable_declaration(consume_semicolon=False)
        self.eat('PUNTOCOMA')
        
        condicion = self.parse_expression()
        self.eat('PUNTOCOMA')
        
        incremento = self.parse_assignment_expression()
        self.eat('PARENTESIS_DER')
        
        cuerpo = self.parse_block_statement()
        
        return {
            'tipo': 'DeclaracionFor',
            'inicializador': inicializador,
            'condicion': condicion,
            'incremento': incremento,
            'cuerpo': cuerpo
        }

    def parse_if_statement(self):
        """
        BNF: <if_statement> ::= IF '(' <expression> ')' <block_statement> [ ELSE <block_statement> ]
        """
        self.eat('IF')
        self.eat('PARENTESIS_IZQ')
        condicion = self.parse_expression()
        self.eat('PARENTESIS_DER')
        
        cuerpo_if = self.parse_block_statement()
        cuerpo_else = None
        
        if self.current_token['tipo'] == 'ELSE':
            self.eat('ELSE')
            cuerpo_else = self.parse_block_statement()
            
        return {'tipo': 'DeclaracionIf', 'condicion': condicion, 'cuerpo_if': cuerpo_if, 'cuerpo_else': cuerpo_else}
            
    def parse_print_statement(self):
        """
        BNF: <print_statement> ::= PRINT '(' <expression> ')' ';'
        """
        self.eat('PRINT')
        self.eat('PARENTESIS_IZQ')
        expression = self.parse_expression()
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaPrint', 'expresion': expression}
    
    def parse_assignment_statement(self):
        """
        BNF: <assignment_statement> ::= ID '=' <expression> ';'
        """
        assignment_node = self.parse_assignment_expression()
        self.eat('PUNTOCOMA')
        return assignment_node

    def parse_function_call(self):
        """
        BNF: <function_call> ::= ID '(' ')' ';'
        """
        function_name = self.current_token['valor']
        self.eat('ID')
        self.eat('PARENTESIS_IZQ')
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaFuncion', 'nombre': function_name}

    # --- INICIO DE MÉTODOS REFACTORIZADOS ---

    def parse_variable_declaration(self, consume_semicolon=True):
        """
        BNF: <variable_declaration> ::= <type> ID '=' <expression> [';']
        """
        data_type = self.current_token
        self.advance() # Avanza después de consumir el tipo de dato
        
        # Llama al método auxiliar para la parte 'ID = <expression>'
        variable_name, value = self._parse_assignment_rhs()
        
        if consume_semicolon:
            self.eat('PUNTOCOMA')
        
        return {'tipo': 'DeclaracionVariable', 'tipo_dato': data_type['valor'], 'nombre': variable_name, 'valor': value}

    def parse_assignment_expression(self):
        """
        Parsea una expresión de asignación como 'ID = <expresion>' sin el punto y coma final.
        """
        # Llama al método auxiliar para la parte 'ID = <expression>'
        variable_name, value = self._parse_assignment_rhs()
        
        return {'tipo': 'Asignacion', 'variable': variable_name, 'valor': value}

    def _parse_assignment_rhs(self):
        """
        Método auxiliar para parsear la parte derecha de una asignación.
        Consume: ID '=' <expression>
        Retorna: (nombre_variable, nodo_valor)
        """
        variable_name = self.current_token['valor']
        self.eat('ID')
        self.eat('IGUAL')
        value = self.parse_expression()
        return variable_name, value

    def parse_expression(self):
        """
        BNF: <expression> ::= <comparison> ( (IGUALIGUAL | DIFERENTE) <comparison> )*
        """
        node = self.parse_comparison()
        while self.current_token['tipo'] in ['IGUALIGUAL', 'DIFERENTE']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_comparison()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_comparison(self):
        """
        BNF: <comparison> ::= <additive_expression> ( (MENOR | MENORIGUAL | MAYOR | MAYORIGUAL) <additive_expression> )*
        """
        node = self.parse_additive_expression()
        while self.current_token['tipo'] in ['MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_additive_expression()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_additive_expression(self):
        """
        BNF: <additive_expression> ::= <multiplicative_expression> ( (MAS | MENOS) <multiplicative_expression> )*
        (Esta era tu antigua parse_expression)
        """
        node = self.parse_multiplicative_expression()
        while self.current_token['tipo'] in ['MAS', 'MENOS']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_multiplicative_expression()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_multiplicative_expression(self):
        """
        BNF: <multiplicative_expression> ::= <primary> ( (POR | DIV) <primary> )*
        (Esta era tu antigua parse_term)
        """
        node = self.parse_primary()
        while self.current_token['tipo'] in ['POR', 'DIV']:
            op_token = self.current_token
            self.advance()
            right_node = self.parse_primary()
            node = {'tipo': 'ExpresionBinaria', 'izquierda': node, 'operador': op_token['tipo'], 'derecha': right_node}
        return node

    def parse_primary(self):
        """
        BNF: <primary> ::= NUMBER | ID | STRING | '(' <expression> ')' | TRUE | FALSE
        (Esta era tu antigua parse_factor)
        """
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
        elif token['tipo'] in ['TRUE', 'FALSE']:
            self.advance() 
            return {'tipo': 'LiteralBooleano', 'valor': token['valor']}
        elif token['tipo'] == 'PARENTESIS_IZQ':
            self.eat('PARENTESIS_IZQ')
            node = self.parse_expression() # Llama a la nueva expresión de nivel superior
            self.eat('PARENTESIS_DER')
            return node
        else:
            raise ParsingError(f"Factor inesperado, no se puede empezar con '{token['tipo']}'")