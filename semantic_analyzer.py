# semantic_analyzer.py

class SemanticError(Exception):
    """
    Una excepción personalizada para errores de significado o lógicos,
    como variables no declaradas o tipos incompatibles.
    """
    pass

class SemanticAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador. En el futuro, aquí se crearía
        la Tabla de Símbolos para llevar un registro de las variables y funciones.
        """
        # self.symbol_table = SymbolTable()
        pass

    def analyze(self, ast):
        """
        PUNTO DE ENTRADA: Recibe el Árbol de Sintaxis Abstracta (AST) del parser
        y lo recorre para aplicar las reglas semánticas del lenguaje.
        """
        # La primera regla semántica que verificamos es que la clase tenga un método 'main'.
        # Esta es una regla de "significado", no de estructura.
        if ast and ast['tipo'] == 'DeclaracionClase':
            
            # Buscamos en el cuerpo del AST de la clase si alguno de los miembros
            # es una declaración de método con el nombre 'main'.
            main_found = any(member.get('nombre') == 'main' for member in ast['cuerpo'])
            
            # Si, después de revisar todos los miembros, no se encontró el 'main', lanzamos un error.
            if not main_found:
                raise SemanticError("Error Semántico: No se encontró un método 'public static void main' en la clase.")
        
        # Aquí es donde se añadirían más comprobaciones en el futuro, como:
        # - Verificar que no haya variables declaradas con el mismo nombre.
        # - Asegurarse de que una variable se haya declarado antes de ser usada.
        # - Comprobar que los tipos en una asignación sean compatibles (ej. no asignar un string a un int).