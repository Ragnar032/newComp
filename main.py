# main.py

import json
from src.lexer.lexer import Lexer
from src.parser.parser import Parser, ParsingError
from src.semantic.semantic import Semantic, SemanticError

# Variable Duplicada
codigo_de_prueba = """
public class MiClase {
    public static void main(String[] args) {
        int x = 5;
        int x = 10; // Error aquí
    }
}
"""
"""
# Variable No Declarada
codigo_de_prueba = 
public class MiClase {
    public static void main(String[] args) {
        int y = x; // Error aquí, 'x' no existe
    }
}
"""

"""
# Incompatibilidad de Tipos
codigo_de_prueba = 
public class MiClase {
    public static void main(String[] args) {
        int z = 5 + "hola"; // Error aquí
    }
}
"""

print("--- 1. FASE LÉXICA ---")
analizador_lexico = Lexer()
tokens = analizador_lexico.analizar(codigo_de_prueba)
print("Tokens generados con éxito:")
for token in tokens:
    print(token)

try:
    print("\n--- 2. FASE SINTÁCTICA (Parsing) ---")
    analizador_sintactico = Parser(tokens)
    ast = analizador_sintactico.parse()
    print("AST construido con éxito.")
    print(json.dumps(ast, indent=2))

    print("\n--- 3. FASE SEMÁNTICA ---")
    analizador_semantico = Semantic()
    analizador_semantico.analyze(ast)
    
    print("\nAnálisis completado con éxito. El código es válido.")

except (ParsingError, SemanticError) as e:
    print(f"\nERROR DETECTADO: {e}")