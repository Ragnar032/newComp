# test_errores_lexicos.py

import pytest
from lexer import Lexer
from tokens import Tokens

# --- Grupo de Pruebas para Errores Léxicos ---

def test_error_por_simbolo_invalido():
    """
    Verifica que el lexer detecta un carácter que no pertenece al alfabeto del lenguaje.
    """
    # El carácter '?' es inválido en este lenguaje.
    codigo_con_error = "int edad = 25?;"
    analizador = Lexer()
    tokens = analizador.analizar(codigo_con_error)

    # Buscamos un token de ERROR que mencione el carácter inválido.
    error_encontrado = any(
        t['tipo'] == 'ERROR' and '?' in t['valor'] for t in tokens
    )

    assert error_encontrado, "El lexer no detectó el símbolo inválido '?'"


def test_comportamiento_con_numero_y_punto():
    """
    (Esta es la prueba corregida)
    Verifica que el lexer tokeniza un número y un punto como dos tokens separados,
    ya que este es un error sintáctico, no léxico.
    """
    codigo = "19.99.5"
    analizador = Lexer()
    tokens = analizador.analizar(codigo)

    # El comportamiento léxicamente correcto es generar tres tokens
    expected_tokens = [
        {'tipo': 'NUMBER', 'valor': '19.99'},
        {'tipo': 'PUNTO', 'valor': '.'},
        {'tipo': 'NUMBER', 'valor': '5'}
    ]
    
    tokens_simplificados = [{'tipo': t['tipo'], 'valor': t['valor']} for t in tokens]
    
    assert tokens_simplificados == expected_tokens, "El lexer debería generar 3 tokens separados"


def test_error_por_cadena_de_texto_no_cerrada():
    """
    Verifica que el lexer detecta una cadena de texto a la que le falta la comilla de cierre.
    """
    # La cadena "Hola mundo nunca se cierra.
    codigo_con_error = 'print("Hola mundo);'
    analizador = Lexer()
    tokens = analizador.analizar(codigo_con_error)

    # La implementación actual debería generar un error al no encontrar la comilla de cierre.
    error_encontrado = any(
        t['tipo'] == 'ERROR' for t in tokens
    )
    
    assert error_encontrado, "El lexer no detectó el error de la cadena no cerrada."


def test_ilustrativo_sobre_limites_lexicos():
    """
    Esta prueba sirve para ilustrar que algunos "errores" aparentes, como un
    identificador que empieza con número, son en realidad manejados por el lexer
    dividiéndolos en tokens válidos. El error real es sintáctico.
    """
    # '2variable' no es un token único inválido para este lexer.
    # Es un token NUMBER ('2') seguido de un token ID ('variable').
    codigo = "2variable"
    analizador = Lexer()
    tokens = analizador.analizar(codigo)
    
    expected_tokens = [
        {'tipo': 'NUMBER', 'valor': '2'},
        {'tipo': 'ID', 'valor': 'variable'}
    ]

    tokens_simplificados = [{'tipo': t['tipo'], 'valor': t['valor']} for t in tokens]
    assert tokens_simplificados == expected_tokens