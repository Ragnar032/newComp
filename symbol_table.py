# symbol_table.py

class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def define(self, name, type):
        """
        Registra un nuevo símbolo (variable) en la tabla.
        Esta es la función que detecta las VARIABLES DUPLICADAS.
        """
        print(f"Definiendo '{name}' con tipo '{type}'")
        
        if name in self.symbols:
            return False
            
        self.symbols[name] = Symbol(name, type)
        return True 

    def lookup(self, name):
        """
        Busca un símbolo en la tabla por su nombre.
        Esta es la función que detecta las VARIABLES NO DECLARADAS.
        """
        print(f"Buscando '{name}' en la tabla de símbolos...")
        
        symbol = self.symbols.get(name)
        return symbol