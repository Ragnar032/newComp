# test_lexer.py

import pytest
from lexer import Lexer
from tokens import Tokens # <-- Importante: Importamos la clase Tokens

# --- Pruebas Anteriores (las mantenemos por completitud) ---

def test_declaracion_completa_correcta():
    codigo = "int valor = 100;"
    analizador = Lexer()
    tokens = analizador.analizar(codigo)
    expected_tokens = [
        {'tipo': 'INT', 'valor': 'int'},
        {'tipo': 'ID', 'valor': 'valor'},
        {'tipo': 'IGUAL', 'valor': '='},
        {'tipo': 'NUMBER', 'valor': '100'},
        {'tipo': 'PUNTOCOMA', 'valor': ';'}
    ]
    tokens_simplificados = [{'tipo': t['tipo'], 'valor': t['valor']} for t in tokens]
    assert tokens_simplificados == expected_tokens

def test_caracter_inesperado():
    codigo = "boolean error = false $;"
    analizador = Lexer()
    tokens = analizador.analizar(codigo)
    error_encontrado = any(t['tipo'] == 'ERROR' and '$' in t['valor'] for t in tokens)
    assert error_encontrado, "No se generó el token de error para el carácter '$'"

def test_cadena_sin_cerrar():
    codigo = 'print("Hola mundo;'
    analizador = Lexer()
    tokens = analizador.analizar(codigo)
    error_encontrado = any(t['tipo'] == 'ERROR' for t in tokens)
    assert error_encontrado, "No se detectó un error para la cadena sin cerrar"

# --- NUEVA PRUEBA PARAMETRIZADA PARA PALABRAS RESERVADAS ---

# El decorador @pytest.mark.parametrize ejecuta la prueba de abajo
# una vez por cada elemento en Tokens.reservadas.items()
@pytest.mark.parametrize("palabra, tipo_esperado", Tokens.reservadas.items())
def test_palabras_reservadas(palabra, tipo_esperado):
    """
    Esta única prueba verifica TODAS las palabras reservadas ('if', 'class', 'while', etc.).
    """
    analizador = Lexer()
    tokens = analizador.analizar(palabra)

    # 1. Verificamos que se haya generado exactamente un token
    assert len(tokens) == 1, f"Se esperaba 1 token para '{palabra}', pero se obtuvieron {len(tokens)}"
    
    token_obtenido = tokens[0]

    # 2. Verificamos que el tipo del token sea el correcto (e.g., 'CLASS' para 'class')
    assert token_obtenido['tipo'] == tipo_esperado
    
    # 3. Verificamos que el valor (lexema) sea la palabra exacta que probamos
    assert token_obtenido['valor'] == palabra