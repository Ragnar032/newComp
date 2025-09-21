# test_errores_lexicos.py

import pytest
from lexer import Lexer

# --- Lista de Casos de Prueba de Errores ---
# Cada tupla contiene: (el código con error, el texto que esperamos ver en el mensaje de error)
casos_de_error_lexico = [
    pytest.param("int mi_var? = 10;", "?", id="símbolo_invalido"),
    pytest.param('print("cadena sin cerrar);', 'Cadena no cerrada', id="cadena_no_cerrada"),
    # Puedes agregar más casos aquí a medida que mejores tu lexer
    # pytest.param("double val = 1.2.3;", "Número mal formado", id="numero_mal_formado"),
]

@pytest.mark.parametrize("codigo_erroneo, texto_esperado_en_error", casos_de_error_lexico)
def test_deteccion_y_mensaje_de_errores_lexicos(codigo_erroneo, texto_esperado_en_error):
    """
    Esta única prueba verifica múltiples tipos de errores léxicos
    y asegura que el mensaje de error sea el correcto.
    """
    print(f"\n--- Probando código: '{codigo_erroneo}' ---") # Este print lo veremos con el comando -s
    analizador = Lexer()
    tokens = analizador.analizar(codigo_erroneo)
    
    # 1. Buscar el token de error en la lista de resultados
    error_token = None
    for token in tokens:
        if token['tipo'] == 'ERROR':
            error_token = token
            break # Encontramos el error, dejamos de buscar

    # 2. Verificar que efectivamente se encontró un token de ERROR
    assert error_token is not None, f"No se generó un token de ERROR para el código problemático."

    # 3. Verificar que el mensaje de error contiene el texto que esperábamos
    valor_del_error = error_token['valor']
    print(f"Mensaje de error obtenido: '{valor_del_error}'") # Veremos este print también
    
    assert texto_esperado_en_error in valor_del_error, \
        f"El mensaje de error no contiene el texto esperado ('{texto_esperado_en_error}')."
# test_lexer.py

def test_analizador_con_archivo_vacio():
    """
    Verifica que el analizador maneja correctamente un archivo (string) vacío
    y devuelve una lista de tokens vacía.
    """
    # 1. Arrange: Preparamos el código de prueba, que es un string vacío.
    codigo_vacio = ""
    analizador = Lexer()

    # 2. Act: Ejecutamos el analizador.
    tokens = analizador.analizar(codigo_vacio)

    # 3. Assert: Verificamos que la lista de tokens esté vacía.
    assert len(tokens) == 0, "El analizador debería devolver una lista vacía para un archivo vacío."