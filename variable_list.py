# variable_list.py
# Gestiona una lista de variables para revisar duplicados y su existencia.

class Variable:
    """Representa una única variable con su nombre y tipo."""
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

class VariableList:
    """Administra una colección de variables para asegurar que sean únicas."""
    def __init__(self):
        # Usamos un diccionario para búsquedas rápidas por nombre.
        self.variables = {}

    def add_variable(self, nombre, tipo):
        """
        Añade una nueva variable a la lista.

        Esta función se usa para detectar VARIABLES DUPLICADAS. Si el nombre
        de la variable ya existe, la función devuelve False.
        """
        print(f"Añadiendo variable '{nombre}' con tipo '{tipo}'")

        if nombre in self.variables:
            # Este nombre de variable ya ha sido añadido.
            return False

        self.variables[nombre] = Variable(nombre, tipo)
        return True

    def find_variable(self, nombre):
        """
        Busca una variable en la lista por su nombre.

        Esta función se usa para detectar VARIABLES NO DECLARADAS. Si la
        variable no se encuentra, la función devuelve None.
        """
        print(f"Buscando '{nombre}' en la lista de variables...")

        variable = self.variables.get(nombre)
        return variable