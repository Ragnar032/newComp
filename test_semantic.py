# test_semantic.py

import pytest
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic import Semantic, SemanticError

# --- Función de Ayuda ---
def run_compiler_phases(code):
    lexer = Lexer()
    tokens = lexer.analizar(code)
    parser = Parser(tokens)
    ast = parser.parse()
    semantic = Semantic()
    semantic.analyze(ast)

# --- Casos de Prueba Válidos ---

def test_valid_code_simple():
    code = """
    public class Main {
        public static void main(String[] args) {
            int a = 10;
            double b = 20.5;
            double c = a + b;
        }
    }
    """
    run_compiler_phases(code)

def test_valid_int_to_double_assignment():
    code = """
    public class Main {
        public static void main(String[] args) {
            int entero = 5;
            double flotante = 0.0;
            flotante = entero;
        }
    }
    """
    run_compiler_phases(code)


# --- Casos de Prueba Inválidos ---

def test_error_duplicate_variable():
    """Verifica que se detecte una variable duplicada."""
    code = """
    public class Main {
        public static void main(String[] args) {
            int x = 5;
            String x = "hola";
        }
    }
    """
    print("\n--- Probando error de variable duplicada ---")
    print("Código a probar:")
    print(code)
    
    with pytest.raises(SemanticError, match="La variable 'x' ya ha sido declarada") as excinfo:
        run_compiler_phases(code)
    
    print(f"✅ Error capturado correctamente: {excinfo.value}")

def test_error_undeclared_variable():
    """Verifica que se detecte el uso de una variable no declarada."""
    code = """
    public class Main {
        public static void main(String[] args) {
            int a = y;
        }
    }
    """
    print("\n--- Probando error de variable no declarada ---")
    print("Código a probar:")
    print(code)

    with pytest.raises(SemanticError, match="La variable 'y' no ha sido declarada") as excinfo:
        run_compiler_phases(code)
        
    print(f"✅ Error capturado correctamente: {excinfo.value}")

def test_error_type_mismatch_assignment():
    """Verifica la detección de tipos incompatibles en una asignación."""
    code = """
    public class Main {
        public static void main(String[] args) {
            int numero = "texto";
        }
    }
    """
    print("\n--- Probando error de incompatibilidad en asignación ---")
    print("Código a probar:")
    print(code)
    
    with pytest.raises(SemanticError, match="No se puede asignar un valor de tipo 'String' a una variable de tipo 'int'") as excinfo:
        run_compiler_phases(code)

    print(f"✅ Error capturado correctamente: {excinfo.value}")

def test_error_type_mismatch_operation():
    """Verifica la detección de tipos incompatibles en una operación binaria."""
    code = """
    public class Main {
        public static void main(String[] args) {
            int resultado = 10 + "hola";
        }
    }
    """
    print("\n--- Probando error de incompatibilidad en operación ---")
    print("Código a probar:")
    print(code)

    with pytest.raises(SemanticError, match="No se puede aplicar el operador 'MAS' a los tipos 'int' y 'String'") as excinfo:
        run_compiler_phases(code)

    print(f"✅ Error capturado correctamente: {excinfo.value}")