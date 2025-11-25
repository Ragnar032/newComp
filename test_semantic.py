# test_semantic.py
import pytest
import sys
sys.path.append('.')

# Importamos tus módulos
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic import Semantic, SemanticError

# Función auxiliar para correr el compilador
def run_compiler_phases(code):
    lexer = Lexer()
    tokens = lexer.analizar(code)
    parser = Parser(tokens)
    ast = parser.parse()
    semantic = Semantic()
    semantic.analyze(ast)

# ==========================================
# CASOS DE PRUEBA (Con impresión de errores)
# ==========================================

def test_caso_1_variable_no_declarada():
    print("\n----------------------------------------------------------------")
    print("PRUEBA 1: Variable No Declarada")
    print("----------------------------------------------------------------")
    
    code = """
    public class Test {
        public static void main(String[] args) {
            a = 10; 
        }
    }
    """
    
    # Verificamos que lance el error y lo capturamos en 'excinfo'
    with pytest.raises(SemanticError, match="La variable 'a' no ha sido declarada") as excinfo:
        run_compiler_phases(code)
    
    # IMPRIMIR EL ERROR EN CONSOLA
    print(f"✅ ÉXITO: El compilador detectó el error correctamente.")
    print(f"   Mensaje recibido: \"{excinfo.value}\"")


def test_caso_2_tipos_incompatibles():
    print("\n----------------------------------------------------------------")
    print("PRUEBA 2: Tipos Incompatibles")
    print("----------------------------------------------------------------")
    
    code = """
    public class Main {
        public static void main(String[] args) {
            int numero = "texto"; 
        }
    }
    """
    
    expected_msg = "Asignación inválida. Variable 'numero' es 'int' pero la expresión es 'String'"
    
    with pytest.raises(SemanticError, match=expected_msg) as excinfo:
        run_compiler_phases(code)

    # IMPRIMIR EL ERROR EN CONSOLA
    print(f"✅ ÉXITO: El compilador detectó el error correctamente.")
    print(f"   Mensaje recibido: \"{excinfo.value}\"")


def test_caso_3_variable_duplicada():
    print("\n----------------------------------------------------------------")
    print("PRUEBA 3: Variable Duplicada")
    print("----------------------------------------------------------------")
    
    code = """
    public class Test {
        public static void main(String[] args) {
            int contador = 100;
            int contador = 50;
        }
    }
    """
    
    with pytest.raises(SemanticError, match="La variable 'contador' ya ha sido declarada") as excinfo:
        run_compiler_phases(code)
    
    # IMPRIMIR EL ERROR EN CONSOLA
    print(f"✅ ÉXITO: El compilador detectó el error correctamente.")
    print(f"   Mensaje recibido: \"{excinfo.value}\"")