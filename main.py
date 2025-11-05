# main.py
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_stack import SemanticStack
from src.postfix_visitor import FullPostfixVisitor 
from src.parser.parser_auxiliaries import ParsingError
from src.semantic.semantic import SemanticError

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
        print("\n--- 1. FASE LÉXICA ---")
        lexer = Lexer()
        tokens = lexer.analizar(codigo_fuente)

        print("\n--- 2. FASE SINTÁCTICA ---")
        parser = Parser(tokens)
        ast = parser.parse()
        print("AST generado con éxito.")
        
        print("\n--- 3. FASE SEMÁNTICA ---")
        semantic = SemanticStack()
        semantic.analyze(ast)
        print("Análisis semántico completado con éxito.")

        print("\n--- 4. FASE DE POSTFIJO DE INSTRUCCIONES ---")
        
        visitor = FullPostfixVisitor()
        visitor.visit(ast) 

    except (ParsingError, SemanticError, Exception) as e:
        print(f"\n--- ERROR DE COMPILACIÓN ---")
        print(e)