# variable_list.py

class Variable:
    def __init__(self, nombre, tipo):
        self.nombre = nombre
        self.tipo = tipo

class VariableList:
    def __init__(self):
        self.variables = {}

    def add_variable(self, nombre, tipo):
        if nombre in self.variables:
            return False

        self.variables[nombre] = Variable(nombre, tipo)
        return True

    def find_variable(self, nombre):
        variable = self.variables.get(nombre)
        return variable