# src/parser/parser.py

from .grammar_rules import GrammarRules
from .parser_auxiliaries import ParsingError # Importar la excepción para el main.py

class Parser(GrammarRules):
    """
    Capa superior y punto de entrada público para el análisis sintáctico.
    Hereda toda la funcionalidad de las capas inferiores.
    """
    def parse(self):
        """
        Punto de entrada principal. Inicia el análisis y realiza 
        comprobaciones finales.
        """
        ast = self.parse_class_declaration()
        
        if self.current_token['tipo'] != 'EOF':
            raise ParsingError(f"Caracteres inesperados ('{self.current_token['valor']}') después del final de la clase.")
        
        # Validación semántica simple: asegurar que existe un método main
        main_found = any(member.get('nombre') == 'main' for member in ast['cuerpo'])
        if not main_found:
            raise ParsingError("No se encontró un método 'public static void main' en la clase.")

        print("Análisis sintáctico completado con éxito.")
        return ast