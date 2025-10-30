# main.py (Limpio, sin TAC/Cuádruplos)

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_stack import SemanticStack
from src.postfix_visitor import FullPostfixVisitor # <- Importa el visitante
from src.parser.parser_auxiliaries import ParsingError
from src.semantic.semantic import SemanticError

# --- TU CÓDIGO FUENTE DE PRUEBA ---
codigo_fuente = """
public class Test {
    public static void main(String[] args) {
        int a = 5;
        double b = (a + 10) * 2;
        
        if (b > 20) {
            print(a);
        } else {
            print(b);
        }
    }
}
"""

if __name__ == "__main__":
    print("--- INICIANDO COMPILADOR ---")
    
    try:
        # 1. LEXER
        print("\n--- 1. FASE LÉXICA ---")
        lexer = Lexer()
        tokens = lexer.analizar(codigo_fuente)

        # 2. PARSER
        print("\n--- 2. FASE SINTÁCTICA ---")
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST generado con éxito.")
        
        # 3. SEMÁNTICA
        print("\n--- 3. FASE SEMÁNTICA ---")
        semantic = SemanticStack()
        semantic.analyze(ast)
        print("Análisis semántico completado con éxito.")

        # 4. IMPRESIÓN DE POSTFIJO COMPLETO
        print("\n--- 4. FASE DE POSTFIJO DE INSTRUCCIONES ---")
        
        visitor = FullPostfixVisitor()
        visitor.visit(ast) # Ejecuta el visitante sobre el AST

    except (ParsingError, SemanticError, Exception) as e:
        print(f"\n--- ERROR DE COMPILACIÓN ---")
        print(e)