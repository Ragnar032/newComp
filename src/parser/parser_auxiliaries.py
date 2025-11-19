# src/parser/parser_auxiliaries.py

class ParsingError(Exception):
    pass

class ParserAuxiliaries:
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

    def peek(self):
            peek_pos = self.pos + 1
            if peek_pos < len(self.tokens):
                return self.tokens[peek_pos]
            else:
                
                return {'tipo': 'EOF', 'valor': None}
        
    def eat(self, token_type):
        if self.current_token and self.current_token['tipo'] == token_type:
            self.advance()
        else:
            expected = token_type
            found = self.current_token['tipo'] if self.current_token else 'EOF'
            raise ParsingError(f"Se esperaba el token '{expected}', pero se encontró '{found}'")