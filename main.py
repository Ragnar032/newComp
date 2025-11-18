# main.py
import os
import json
import sys

sys.path.append('.')

from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.semantic.semantic_stack import SemanticStack
from src.postfix_visitor import FullPostfixVisitor 
from src.parser.parser_auxiliaries import ParsingError
from src.semantic.semantic import SemanticError
from src.optimizer.constant_folder import ConstantFolder 

def guardar_json(data, carpeta, nombre_archivo):
    os.makedirs(carpeta, exist_ok=True)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"   [OK] Archivo guardado en: {ruta_completa}")
    except Exception as e:
        print(f"   [ERROR] No se pudo guardar el archivo {nombre_archivo}: {e}")

codigo_fuente = """
public class Test {
    public static void main(String[] args) {
        int a = 5;
        // Operación constante: (5 + 10) * 2 debe convertirse en 30.0
        double b = (5 + 10) * 2; 
        
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
        # ---------------------------------------------------------
        # 1. FASE LÉXICA
        # ---------------------------------------------------------
        print("\n--- 1. FASE LÉXICA ---")
        lexer = Lexer()
        tokens = lexer.analizar(codigo_fuente)
        print(f"   Tokens generados: {len(tokens)}")
        
        guardar_json(tokens, "resultados/tokens", "lista_tokens.json")


        # ---------------------------------------------------------
        # 2. FASE SINTÁCTICA
        # ---------------------------------------------------------
        print("\n--- 2. FASE SINTÁCTICA ---")
        parser = Parser(tokens)
        ast = parser.parse()
        print("   AST generado con éxito.")

        # Guardar AST Original
        guardar_json(ast, "resultados/ast", "ast_original.json")
        
        
        # ---------------------------------------------------------
        # 3. FASE SEMÁNTICA
        # ---------------------------------------------------------
        print("\n--- 3. FASE SEMÁNTICA ---")
        semantic = SemanticStack()
        semantic.analyze(ast)
        print("   Análisis semántico completado con éxito.")


        # ---------------------------------------------------------
        # 4. GENERACIÓN DE CÓDIGO INTERMEDIO (ANTES DE OPTIMIZAR)
        # ---------------------------------------------------------
        print("\n--- 4. CÓDIGO INTERMEDIO (SIN OPTIMIZAR) ---")
        visitor = FullPostfixVisitor()
        visitor.visit(ast) 


        # ---------------------------------------------------------
        # 5. FASE DE OPTIMIZACIÓN (Constant Folding)
        # ---------------------------------------------------------
        print("\n--- 5. APLICANDO OPTIMIZACIÓN: CÁLCULO DE CONSTANTES ---")
        optimizer = ConstantFolder()
        ast_optimizado = optimizer.optimize(ast)
        
        guardar_json(ast_optimizado, "resultados/ast", "ast_optimizado.json")
        print("   AST optimizado generado.")


        # ---------------------------------------------------------
        # 6. GENERACIÓN DE CÓDIGO INTERMEDIO (DESPUÉS DE OPTIMIZAR)
        # ---------------------------------------------------------
        print("\n--- 6. CÓDIGO INTERMEDIO (OPTIMIZADO) ---")
        visitor_opt = FullPostfixVisitor()
        visitor_opt.visit(ast_optimizado)


    except (ParsingError, SemanticError) as e:
        print(f"\n--- ERROR DE LÓGICA DE COMPILACIÓN ---")
        print(e)
    except Exception as e:
        print(f"\n--- ERROR INTERNO ---")
        import traceback
        traceback.print_exc()