# src/parser/parser_auxiliaries.py

class ParsingError(Exception):
    """Excepción personalizada para errores de sintaxis."""
    pass

class ParserAuxiliaries:
    """Capa base que gestiona el estado del parser y las funciones auxiliares."""
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        """Avanza al siguiente token en la lista."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = {'tipo': 'EOF', 'valor': None}
    
    def eat(self, token_type):
        """
        Consume el token actual si es del tipo esperado.
        Si no, lanza un ParsingError.
        """
        if self.current_token and self.current_token['tipo'] == token_type:
            self.advance()
        else:
            expected = token_type
            found = self.current_token['tipo'] if self.current_token else 'EOF'
            raise ParsingError(f"Se esperaba el token '{expected}', pero se encontró '{found}'")