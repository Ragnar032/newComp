# main.py

import json
from lexer import Lexer
from parser import Parser, ParsingError
# Ya no importamos el analizador semántico

# --- CÓDIGO FUENTE A COMPILAR ---
codigo_de_prueba = """
public class MiClase {
    public static void main(String[] args) {
        int resultado = 5 + 10;
    }
}
"""

print("--- 1. FASE LÉXICA ---")
analizador_lexico = Lexer()
tokens = analizador_lexico.analizar(codigo_de_prueba)

# Imprimimos los tokens en formato simple
for token in tokens:
    print(token)

# Bloque try-except solo para errores de parsing
try:
    print("\n--- 2. FASE SINTÁCTICA (Parsing) ---")
    analizador_sintactico = Parser(tokens)
    ast = analizador_sintactico.parse()
    print("AST construido con éxito.")
    # Imprimimos el AST para ver el resultado del parser
    print(json.dumps(ast, indent=2))
    
    print("\nAnálisis sintáctico completado con éxito.")

except ParsingError as e:
    # Si ocurre un error sintáctico, se captura aquí
    print(f"\nERROR SINTÁCTICO DETECTADO: {e}")