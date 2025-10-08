# variable_list.py
# Gestiona una lista de variables para revisar duplicados y su existencia.

class Variable:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

class VariableList:
    def __init__(self):
        self.variables = {}

    def add_variable(self, nombre, tipo):
        print(f"Añadiendo variable '{nombre}' con tipo '{tipo}'")

        if nombre in self.variables:
            # Este nombre de variable ya ha sido añadido.
            return False

        self.variables[nombre] = Variable(nombre, tipo)
        return True

    def find_variable(self, nombre):
        print(f"Buscando '{nombre}' en la lista de variables...")

        variable = self.variables.get(nombre)
        return variable