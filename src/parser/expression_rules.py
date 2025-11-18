# src/parser/expression_rules.py
from .parser_auxiliaries import ParserAuxiliaries, ParsingError

class ExpressionRules(ParserAuxiliaries):


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
            node = self.parse_expression()
            self.eat('PARENTESIS_DER')
            return node
        else:
            raise ParsingError(f"Factor inesperado, no se puede empezar con '{token['tipo']}'")