# src/lexer/lexer.py

from .matriz_transicion import MatrizTransicion

class Lexer:
    """
    Interfaz pública para el analizador léxico.
    Utiliza un motor de matriz de transición para realizar el análisis.
    """
    def __init__(self):
        self.motor_matriz = MatrizTransicion()

    def analizar(self, codigo_fuente):
        """
        Toma el código fuente como una cadena y devuelve una lista de tokens.
        """
        return self.motor_matriz.analizar(codigo_fuente)