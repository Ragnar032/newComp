# symbol_table.py

# NOTA: Un 'Símbolo' es un objeto que guarda información sobre una variable o función.
# Por ahora, solo nos importa su nombre y su tipo (ej. 'x', 'int').
class Symbol:
    def __init__(self, name, type):
        self.name = name
        self.type = type

# NOTA: La 'Tabla de Símbolos' es como la memoria del compilador. Es un diccionario
# donde guardamos todos los símbolos que se han declarado.
class SymbolTable:
    def __init__(self):
        # Usamos un diccionario de Python. La clave será el nombre del símbolo (ej. 'x')
        # y el valor será el objeto Symbol completo.
        self.symbols = {}

    def define(self, name, type):
        """
        Registra un nuevo símbolo (variable) en la tabla.
        Esta es la función que detecta las VARIABLES DUPLICADAS.
        """
        print(f"Definiendo '{name}' con tipo '{type}'")
        
        # Comprobamos si el nombre ya existe en nuestro diccionario de símbolos.
        if name in self.symbols:
            # Si ya existe, no podemos declararlo de nuevo. Devolvemos False para indicar el error.
            return False
            
        # Si no existe, creamos un nuevo objeto Symbol y lo guardamos en la tabla.
        self.symbols[name] = Symbol(name, type)
        return True # Devolvemos True para indicar que la definición fue exitosa.

    def lookup(self, name):
        """
        Busca un símbolo en la tabla por su nombre.
        Esta es la función que detecta las VARIABLES NO DECLARADAS.
        """
        print(f"Buscando '{name}' en la tabla de símbolos...")
        
        # Usamos .get() en el diccionario. Si encuentra el símbolo, lo devuelve.
        # Si no lo encuentra, devuelve None, lo que significa que la variable no ha sido declarada.
        symbol = self.symbols.get(name)
        return symbol