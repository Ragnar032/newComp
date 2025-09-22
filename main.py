# main.py

import json
from lexer import Lexer
from parser import Parser, ParsingError
from semantic_analyzer import SemanticAnalyzer, SemanticError



#Variable Duplicada
codigo_de_prueba = """
public class MiClase {
    public static void main(String[] args) {
        int x = 5;
        int x = 10; // Error aquí
    }
}
"""
"""
#Variable No Declarada
codigo_de_prueba = 
public class MiClase {
    public static void main(String[] args) {
        int y = x; // Error aquí, 'x' no existe
    }
}
"""


"""
#Incompatibilidad de Tipos
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
# Imprime la lista de tokens, uno por línea
for token in tokens:
    print(token)

# Bloque try-except para capturar errores de las fases de parsing y semántica
try:
    print("\n--- 2. FASE SINTÁCTICA (Parsing) ---")
    analizador_sintactico = Parser(tokens)
    ast = analizador_sintactico.parse()
    print("AST construido con éxito.")
    # Imprimimos el AST para ver el resultado del parser
    print(json.dumps(ast, indent=2))

    print("\n--- 3. FASE SEMÁNTICA ---")
    analizador_semantico = SemanticAnalyzer()
    analizador_semantico.analyze(ast)
    
    print("\nAnálisis completado con éxito. El código es válido.")

except (ParsingError, SemanticError) as e:
    # Si ocurre un error sintáctico o semántico, se captura aquí
    print(f"\nERROR DETECTADO: {e}")