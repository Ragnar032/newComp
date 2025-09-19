# state_machine.py

from tokens import Tokens

class StateMachine:
    def __init__(self):
        self.reservadas = Tokens.reservadas
        self.simbolos_simples = {
            '+': 'MAS', '-': 'MENOS', '*': 'POR', '/': 'DIV', '%': 'MOD',
            '(': 'PARENTESIS_IZQ', ')': 'PARENTESIS_DER',
            '{': 'LLAVE_IZQ', '}': 'LLAVE_DER',
            '[': 'CORCHETE_IZQ', ']': 'CORCHETE_DER',
            ';': 'PUNTOCOMA', '.': 'PUNTO', ',': 'COMA'
        }

    def get_next_token(self, codigo, pos, linea):
        """
        Analiza el código desde una posición para encontrar el siguiente token.
        Devuelve: (token, nueva_posicion, nueva_linea)
        Si no hay token (ej. espacio en blanco), devuelve (None, nueva_pos, nueva_linea).
        """
        if pos >= len(codigo):
            return (None, pos, linea)

        caracter_actual = codigo[pos]

        # 1. Ignorar espacios en blanco
        if caracter_actual.isspace():
            nueva_linea = linea + 1 if caracter_actual == '\n' else linea
            return (None, pos + 1, nueva_linea)

        # 2. Identificadores y Palabras Reservadas
        if caracter_actual.isalpha():
            return self._process_identifier(codigo, pos, linea)

        # 3. Números (Enteros y Doubles)
        if caracter_actual.isdigit():
            return self._process_number(codigo, pos, linea)
        
        # 4. Cadenas
        if caracter_actual == '"':
            return self._process_string(codigo, pos, linea)

        # 5. Operadores de dos caracteres (con lookahead)
        token_dos_chars = self._process_two_char_operator(codigo, pos, linea)
        if token_dos_chars:
            return token_dos_chars
        
        # 6. Símbolos y operadores de un caracter
        if caracter_actual in self.simbolos_simples:
            tipo = self.simbolos_simples[caracter_actual]
            token = {'tipo': tipo, 'valor': caracter_actual, 'linea': linea}
            return (token, pos + 1, linea)
        
        # 7. Operadores de un caracter que pueden ser parte de uno de dos
        if caracter_actual in "=!<>":
             # Si no formó uno de dos caracteres, es uno simple
            tipos = {'=': 'IGUAL', '!': 'NOT', '<': 'MENOR', '>': 'MAYOR'}
            token = {'tipo': tipos[caracter_actual], 'valor': caracter_actual, 'linea': linea}
            return (token, pos + 1, linea)

        # 8. Si nada coincide, es un error
        token_error = {'tipo': 'ERROR', 'valor': f"Caracter inesperado: '{caracter_actual}'", 'linea': linea}
        return (token_error, pos + 1, linea)

    # --- Métodos de ayuda privados ---

    def _process_identifier(self, codigo, pos, linea):
        lexema = codigo[pos]
        pos += 1
        while pos < len(codigo) and (codigo[pos].isalnum() or codigo[pos] == '_'):
            lexema += codigo[pos]
            pos += 1
        
        tipo_token = self.reservadas.get(lexema, 'ID')
        token = {'tipo': tipo_token, 'valor': lexema, 'linea': linea}
        return (token, pos, linea)

    def _process_number(self, codigo, pos, linea):
        lexema = codigo[pos]
        pos += 1
        while pos < len(codigo) and codigo[pos].isdigit():
            lexema += codigo[pos]
            pos += 1
        
        if pos < len(codigo) and codigo[pos] == '.':
            lexema += '.'
            pos += 1
            while pos < len(codigo) and codigo[pos].isdigit():
                lexema += codigo[pos]
                pos += 1
        
        token = {'tipo': 'NUMBER', 'valor': lexema, 'linea': linea}
        return (token, pos, linea)

    def _process_string(self, codigo, pos, linea):
        lexema = ''
        pos += 1 # Omitir la comilla inicial
        while pos < len(codigo) and codigo[pos] != '"':
            lexema += codigo[pos]
            pos += 1
        
        if pos < len(codigo) and codigo[pos] == '"':
            token = {'tipo': 'CADENA', 'valor': lexema, 'linea': linea}
            return (token, pos + 1, linea) # Omitir la comilla final
        else:
            token_error = {'tipo': 'ERROR', 'valor': 'Cadena no cerrada', 'linea': linea}
            return (token_error, pos, linea)

    def _process_two_char_operator(self, codigo, pos, linea):
        if pos + 1 < len(codigo):
            dos_chars = codigo[pos:pos+2]
            tipos = {
                '==': 'IGUALIGUAL', '!=': 'DIFERENTE', '<=': 'MENORIGUAL',
                '>=': 'MAYORIGUAL', '&&': 'AND', '||': 'OR'
            }
            if dos_chars in tipos:
                token = {'tipo': tipos[dos_chars], 'valor': dos_chars, 'linea': linea}
                return (token, pos + 2, linea)
        return None
    
    #error de archivo vacio
    #error si hay mas caracteres despues de terminar el codiggo
    #error inicia con numero
    #si hay un metodo fuera dle main error o caracter fuera del main error
    