# parser.py

# ... (ParsingError, Parser, init, advance, eat se mantienen igual) ...
class ParsingError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = {'tipo': 'EOF', 'valor': None}
    
    def eat(self, token_type):
        if self.current_token and self.current_token['tipo'] == token_type:
            self.advance()
        else:
            expected = token_type
            found = self.current_token['tipo'] if self.current_token else 'EOF'
            raise ParsingError(f"Se esperaba el token '{expected}', pero se encontró '{found}'")


 

    def parse_expression(self):
        """
        Analiza una expresión de suma y resta.
        BNF: <expresion> ::= <termino> | <expresion> "+" <termino> | <expresion> "-" <termino>
        """
        # Comienza analizando el primer término
        node = self.parse_term()

        # Mientras el siguiente token sea + o -, sigue construyendo el árbol de expresión
        while self.current_token['tipo'] in ['MAS', 'MENOS']:
            op_token = self.current_token
            self.advance() # Consume el '+' o '-'
            
            right_node = self.parse_term()
            
            # Crea un nodo de operación binaria y lo asigna como el nuevo nodo principal
            node = {
                'tipo': 'ExpresionBinaria',
                'izquierda': node,
                'operador': op_token['tipo'],
                'derecha': right_node
            }
        
        return node

    def parse_term(self):
        """
        Analiza un término de multiplicación y división.
        BNF: <termino> ::= <factor> | <termino> "*" <factor> | <termino> "/" <factor>
        """
        node = self.parse_factor()

        while self.current_token['tipo'] in ['POR', 'DIV']:
            op_token = self.current_token
            self.advance() # Consume el '*' o '/'
            
            right_node = self.parse_factor()
            
            node = {
                'tipo': 'ExpresionBinaria',
                'izquierda': node,
                'operador': op_token['tipo'],
                'derecha': right_node
            }
            
        return node

    def parse_factor(self):
        """
        Analiza un factor, la unidad más pequeña de una expresión.
        BNF: <factor> ::= <identificador> | <numero> | "(" <expresion> ")"
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
        elif token['tipo'] == 'PARENTESIS_IZQ':
            self.eat('PARENTESIS_IZQ')
            node = self.parse_expression() # Llama recursivamente a la regla de expresión
            self.eat('PARENTESIS_DER')
            return node
        else:
            raise ParsingError(f"Factor inesperado, no se puede empezar con '{token['tipo']}'")



    # --- El resto de las funciones (parse, parse_class_declaration, etc.)
    # --- se benefician de este cambio pero no necesitan ser modificadas por ahora.
    # --- (Se omiten por brevedad, pero deben permanecer en tu archivo)
    def parse(self):
        """
        PUNTO DE ENTRADA: Inicia el análisis y realiza validaciones finales.
        """
        # Llama a la regla inicial de la gramática.
        ast = self.parse_class_declaration()
        
        # Después de analizar la clase, no debería quedar nada más.
        if self.current_token['tipo'] != 'EOF':
            raise ParsingError(f"Caracteres inesperados ('{self.current_token['valor']}') después del final de la clase.")
        
        # Verificación semántica final sobre el AST construido.
        main_found = any(member.get('nombre') == 'main' for member in ast['cuerpo'])
        if not main_found:
            raise ParsingError("Error Semántico: No se encontró un método 'public static void main' en la clase.")

        print("Análisis sintáctico y semántico completado con éxito.")
        return ast

    def parse_class_declaration(self):
        """
        Analiza una declaración de clase.
        BNF: <declaracion_clase> ::= PUBLIC CLASS ID LLAVE_IZQ <cuerpo_clase> LLAVE_DER
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
        Decide qué tipo de miembro de la clase se está declarando.
        BNF: <miembro_clase> ::= <declaracion_metodo> | <declaracion_variable>
        """
        if self.current_token['tipo'] in ['PUBLIC', 'PRIVATE']:
            return self.parse_method_declaration()
        
        data_types = ['INT', 'DOUBLE', 'BOOLEAN', 'STRINGTYPE']
        if self.current_token['tipo'] in data_types:
            return self.parse_variable_declaration()
        
        raise ParsingError(f"Declaración inesperada dentro de la clase, no se puede empezar con '{self.current_token['tipo']}'")

    def parse_method_declaration(self):
        """
        Decide qué tipo de método se está declarando (main u otro).
        """
        self.eat('PUBLIC')
        
        # Esta es una decisión de análisis predictivo: si vemos 'static', debe ser el 'main'.
        if self.current_token['tipo'] == 'STATIC':
            return self.parse_main_method_declaration()
        else:
            return self.parse_generic_method_declaration()

    def parse_main_method_declaration(self):
        """
        Analiza la declaración del método 'main'.
        BNF: <main_method> ::= STATIC VOID MAIN PARENTESIS_IZQ STRINGTYPE CORCHETE_IZQ CORCHETE_DER ID PARENTESIS_DER <bloque>
        """
        self.eat('STATIC')
        self.eat('VOID')
        self.eat('MAIN')
        self.eat('PARENTESIS_IZQ')
        self.eat('STRINGTYPE')
        self.eat('CORCHETE_IZQ')
        self.eat('CORCHETE_DER')
        self.eat('ID') # para 'args'
        self.eat('PARENTESIS_DER')
        
        method_body = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionMetodo', 'nombre': 'main', 'tipo_retorno': 'void', 'cuerpo': method_body}

    def parse_generic_method_declaration(self):
        """
        Analiza una declaración de método genérico.
        BNF: <generic_method> ::= TIPO_RETORNO ID PARENTESIS_IZQ PARENTESIS_DER <bloque>
        """
        return_type = self.current_token['valor']
        self.advance()
        
        method_name = self.current_token['valor']
        self.eat('ID')
        
        self.eat('PARENTESIS_IZQ')
        # Aquí iría el análisis de parámetros
        self.eat('PARENTESIS_DER')
        
        method_body = self.parse_block_statement()
        
        return {'tipo': 'DeclaracionMetodo', 'nombre': method_name, 'tipo_retorno': return_type, 'cuerpo': method_body}

    def parse_block_statement(self):
        """
        Analiza un bloque de sentencias rodeado por llaves.
        BNF: <bloque> ::= LLAVE_IZQ <sentencia>* LLAVE_DER
        """
        self.eat('LLAVE_IZQ')
        statements = []
        while self.current_token['tipo'] != 'LLAVE_DER' and self.current_token['tipo'] != 'EOF':
            statements.append(self.parse_statement())
        self.eat('LLAVE_DER')
        return statements

    def parse_statement(self):
        """
        Decide qué tipo de sentencia se está declarando dentro de un método.
        BNF: <sentencia> ::= <declaracion_variable> | <llamada_print>
        """
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
        """
        Analiza una llamada a la función print.
        BNF: <llamada_print> ::= PRINT PARENTESIS_IZQ <expresion> PARENTESIS_DER PUNTOCOMA
        """
        self.eat('PRINT')
        self.eat('PARENTESIS_IZQ')
        expression = self.parse_expression()
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaPrint', 'expresion': expression}
    
    def parse_function_call(self):
        """
        Analiza una llamada a una función.
        BNF: <llamada_funcion> ::= ID PARENTESIS_IZQ PARENTESIS_DER PUNTOCOMA
        """
        function_name = self.current_token['valor']
        self.eat('ID')
        self.eat('PARENTESIS_IZQ')
        self.eat('PARENTESIS_DER')
        self.eat('PUNTOCOMA')
        return {'tipo': 'LlamadaFuncion', 'nombre': function_name}

    def parse_variable_declaration(self):
        """
        Analiza una declaración de variable.
        BNF: <declaracion_variable> ::= TIPO_DATO ID IGUAL <expresion> PUNTOCOMA
        """
        data_type = self.current_token
        self.advance()
        variable_name = self.current_token
        self.eat('ID')
        self.eat('IGUAL')
        value = self.parse_expression()
        self.eat('PUNTOCOMA')
        return {'tipo': 'DeclaracionVariable', 'tipo_dato': data_type['valor'], 'nombre': variable_name['valor'], 'valor': value}