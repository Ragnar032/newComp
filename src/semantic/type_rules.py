# src/semantic/type_rules.py

# Reglas para operadores aritméticos (+, -, *)
_arithmetic_rules = {
    'int': {'int': 'int', 'double': 'double', 'String': 'error', 'boolean': 'error'},
    'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
}

# Reglas para operadores de división (/)
_division_rules = {
    'int': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
    'double': {'int': 'double', 'double': 'double', 'String': 'error', 'boolean': 'error'},
}

# Reglas para operadores de comparación (<=, >=, <, >)
_comparison_rules = {
    'int': {'int': 'boolean', 'double': 'boolean'},
    'double': {'int': 'boolean', 'double': 'boolean'},
}

# Reglas para operadores de igualdad (==, !=)
_equality_rules = {
    'int': {'int': 'boolean', 'double': 'boolean', 'String': 'error', 'boolean': 'error'},
    'double': {'int': 'boolean', 'double': 'boolean', 'String': 'error', 'boolean': 'error'},
    'String': {'String': 'boolean'}, 
    'boolean': {'boolean': 'boolean'},
}

# 2. Construye el diccionario principal que el semántico usará
TYPE_RULES = {
    'MAS': _arithmetic_rules,
    'MENOS': _arithmetic_rules,
    'POR': _arithmetic_rules,
    'DIV': _division_rules,
    
    'IGUALIGUAL': _equality_rules,
    'DIFERENTE': _equality_rules, # Asumiendo que '!=' usa las mismas reglas que '=='
    
    'MENOR': _comparison_rules,
    'MENORIGUAL': _comparison_rules,
    'MAYOR': _comparison_rules, 
    'MAYORIGUAL': _comparison_rules, 
}