# lexer.py

from matriz_transicion import MatrizTransicion

class Lexer:
    def __init__(self):
        # El lexer ahora delega TODA la lógica a la clase MatrizTransicion
        self.motor_matriz = MatrizTransicion()

    def analizar(self, codigo_fuente):
        # Simplemente llamamos al método de análisis de nuestro motor
        return self.motor_matriz.analizar(codigo_fuente)