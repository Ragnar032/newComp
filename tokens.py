# tokens.py

class Tokens:
    # Palabras reservadas
    reservadas = {
        'class': 'CLASS', 'public': 'PUBLIC', 'private': 'PRIVATE', 'static': 'STATIC',
        'void': 'VOID', 'main': 'MAIN', 'if': 'IF', 'else': 'ELSE', 'while': 'WHILE',
        'for': 'FOR', 'return': 'RETURN', 'print': 'PRINT', 'int': 'INT', 'double': 'DOUBLE',
        'boolean': 'BOOLEAN', 'String': 'STRINGTYPE', 'true': 'TRUE', 'false': 'FALSE',
    }

    # Lista de todos los tipos de tokens
    tokens = [
        'ID', 'NUMBER', 'CADENA', 'MAS', 'MENOS', 'POR', 'DIV', 'MOD', 'IGUAL', 
        'IGUALIGUAL', 'DIFERENTE', 'MENOR', 'MENORIGUAL', 'MAYOR', 'MAYORIGUAL',
        'AND', 'OR', 'NOT', 'PARENTESIS_IZQ', 'PARENTESIS_DER', 'LLAVE_IZQ', 
        'LLAVE_DER', 'CORCHETE_IZQ', 'CORCHETE_DER', 'PUNTOCOMA', 'PUNTO', 'COMA',
    ] + list(reservadas.values())