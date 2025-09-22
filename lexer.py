# lexer.py

from matriz_transicion import MatrizTransicion

class Lexer:
    def __init__(self):
        self.motor_matriz = MatrizTransicion()

    def analizar(self, codigo_fuente):
        return self.motor_matriz.analizar(codigo_fuente)