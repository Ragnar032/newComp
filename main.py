# main.py

from lexer import Lexer
# No necesitas importar json para esta opción

codigo_de_prueba = """
public class Ejemplo {
    public static void main(String[] args) {
        int numero = 100;
        if (numero >= 100) {
            print("OK");
        }
    }
}
"""

analizador = Lexer()
tokens = analizador.analizar(codigo_de_prueba)

# --- Opción 2: Reemplaza el print de json por este bucle ---
print("--- Lista de Tokens ---")
for token in tokens:
    print(token)
print("-----------------------")