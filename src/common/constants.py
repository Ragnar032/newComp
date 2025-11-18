# src/common/constants.py

class OperatorMap:
    MAP = {
        'MAS': '+',
        'MENOS': '-',
        'POR': '*',
        'DIV': '/',
        'IGUALIGUAL': '==',
        'DIFERENTE': '!=',
        'MENOR': '<',
        'MENORIGUAL': '<=',
        'MAYOR': '>',
        'MAYORIGUAL': '>='
    }


    REVERSE_MAP = { v: k for k, v in MAP.items() }