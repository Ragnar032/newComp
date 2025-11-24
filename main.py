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
from src.intermediate.quadruple_generator import QuadrupleGenerator
from src.asm.nasm_generator import NasmGenerator

def guardar_json(data, carpeta, nombre_archivo):
    os.makedirs(carpeta, exist_ok=True)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"   [OK] JSON: {ruta_completa}")
    except Exception as e:
        print(f"   [ERROR] JSON: {e}")

def guardar_texto(texto, carpeta, nombre_archivo):
    os.makedirs(carpeta, exist_ok=True)
    ruta_completa = os.path.join(carpeta, nombre_archivo)
    try:
        with open(ruta_completa, 'w', encoding='utf-8') as f:
            f.write(texto)
        print(f"   [OK] ARCHIVO: {ruta_completa}")
    except Exception as e:
        print(f"   [ERROR] TEXTO: {e}")

RUTA_CODIGO_FUENTE = "source.txt"

if __name__ == "__main__":
    
    if not os.path.exists(RUTA_CODIGO_FUENTE):
        print(f"ERROR: No se encontró el archivo '{RUTA_CODIGO_FUENTE}'.")
        print("Por favor crea este archivo con tu código fuente.")
        sys.exit(1)
        
    with open(RUTA_CODIGO_FUENTE, 'r', encoding='utf-8') as f:
        codigo_fuente = f.read()

    print("--- INICIANDO COMPILADOR (TARGET: NASM Linux x64) ---")
    
    try:
        # ---------------------------------------------------------
        # 1. FASE LÉXICA (Tokenización)
        # ---------------------------------------------------------
        print("\n--- 1. ANÁLISIS LÉXICO ---")
        lexer = Lexer()
        tokens = lexer.analizar(codigo_fuente)
        print(f"   Tokens generados: {len(tokens)}")
        guardar_json(tokens, "resultados/tokens", "tokens.json")

        # ---------------------------------------------------------
        # 2. FASE SINTÁCTICA (Parsing)
        # ---------------------------------------------------------
        print("\n--- 2. ANÁLISIS SINTÁCTICO ---")
        parser = Parser(tokens)
        ast = parser.parse()
        print("   AST generado correctamente.")
        guardar_json(ast, "resultados/ast", "ast_original.json")
        
        # ---------------------------------------------------------
        # 3. FASE SEMÁNTICA
        # ---------------------------------------------------------
        print("\n--- 3. ANÁLISIS SEMÁNTICO ---")
        semantic = SemanticStack()
        semantic.analyze(ast)
        print("   Validación semántica exitosa (Tipos y Variables OK).")

        # ---------------------------------------------------------
        # 4. CÓDIGO INTERMEDIO (Antes de Optimizar - Opcional)
        # ---------------------------------------------------------
        print("\n--- 4. CÓDIGO INTERMEDIO (SIN OPTIMIZAR) ---")
        visitor_crudo = FullPostfixVisitor()
        codigo_crudo = visitor_crudo.visit(ast)
        
        print(">>> INICIO POSTFIJO CRUDO >>>")
        print(codigo_crudo)
        print("<<< FIN POSTFIJO CRUDO <<<")
        guardar_texto(codigo_crudo, "resultados/codigo_intermedio", "postfijo_sin_optimizar.txt")

        # ---------------------------------------------------------
        # 5. FASE DE OPTIMIZACIÓN (Constant Folding)
        # ---------------------------------------------------------
        print("\n--- 5. APLICANDO OPTIMIZACIÓN ---")
        optimizer = ConstantFolder()
        ast_optimizado = optimizer.optimize(ast)
        guardar_json(ast_optimizado, "resultados/ast", "ast_optimizado.json")
        print("   Optimización completada.")

        # ---------------------------------------------------------
        # 6. CÓDIGO INTERMEDIO (OPTIMIZADO)
        # ---------------------------------------------------------
        print("\n--- 6. CÓDIGO INTERMEDIO (POSTFIJO OPTIMIZADO) ---")
        visitor_opt = FullPostfixVisitor()
        codigo_optimizado = visitor_opt.visit(ast_optimizado)
        
        print(">>> INICIO POSTFIJO OPTIMIZADO >>>")
        print(codigo_optimizado)
        print("<<< FIN POSTFIJO OPTIMIZADO <<<")
        guardar_texto(codigo_optimizado, "resultados/codigo_intermedio", "postfijo_optimizado.txt")

        # ---------------------------------------------------------
        # 7. CÓDIGO INTERMEDIO (CUÁDRUPLOS) - ¡AQUÍ ESTÁ LA CLAVE!
        # ---------------------------------------------------------
        print("\n--- 7. CÓDIGO INTERMEDIO (CUÁDRUPLOS) ---")
        quad_gen = QuadrupleGenerator()
        lista_cuadruplos = quad_gen.generate(ast_optimizado)
        
        guardar_json(lista_cuadruplos, "resultados/intermedio", "cuadruplos.json")

        # Imprimir tabla bonita (sin error de NoneType)
        header = f"{'OP':<15} | {'ARG1':<15} | {'ARG2':<15} | {'RES':<15}"
        print("-" * 65)
        print(header)
        print("-" * 65)
        
        texto_tabla = header + "\n" + ("-" * 65) + "\n"
        for q in lista_cuadruplos:
            op = str(q['op'])
            a1 = str(q['arg1']) if q['arg1'] is not None else ""
            a2 = str(q['arg2']) if q['arg2'] is not None else ""
            res = str(q['res']) if q['res'] is not None else ""
            
            linea = f"{op:<15} | {a1:<15} | {a2:<15} | {res:<15}"
            print(linea)
            texto_tabla += linea + "\n"
            
        guardar_texto(texto_tabla, "resultados/intermedio", "tabla_cuadruplos.txt")

        # ---------------------------------------------------------
        # 8. GENERACIÓN DE CÓDIGO FINAL (Backend NASM)
        # ---------------------------------------------------------
        print("\n--- 8. GENERACIÓN DE ENSAMBLADOR (NASM x64) ---")
        if not lista_cuadruplos:
            print("   [!] No hay código intermedio para procesar.")
        else:
            # Instanciamos el Generador
            generator = NasmGenerator()
            
            # CORRECCIÓN: Pasamos la LISTA DE CUÁDRUPLOS, no el string postfijo
            asm_code = generator.generate(lista_cuadruplos)
            
            # Guardamos el resultado final
            guardar_texto(asm_code, "resultados/output", "programa.asm")
            
            print("\n[COMPILACIÓN EXITOSA]")
            print("Copia el contenido de 'resultados/output/programa.asm' y ejecútalo.")

    except (ParsingError, SemanticError) as e:
        print(f"\n[ERROR DE COMPILACIÓN]: {e}")
    except Exception as e:
        print(f"\n[ERROR INTERNO DEL COMPILADOR]: {e}")
        import traceback
        traceback.print_exc()