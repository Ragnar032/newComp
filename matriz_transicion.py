# matriz_transicion.py

from tokens import Tokens

class MatrizTransicion:
    def __init__(self):
        self.reservadas = Tokens.reservadas
        
        # Columnas: 0=L, 1=D, 2=., 3=", 4==, 5=!, 6=<, 7=>, 8=&, 9=|, 10=/, 11=*, 12=OpA, 13=Del, 14=WS, 15=Otro
        self.matriz = [
          #    0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15
            [ 1,  2, 21, 11,  3,  4,  5,  6,  7,  8, 22, 13, 13, 14,  0, -1], # S0
            [ 1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S1
            [-1,  2,  9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S2
            [-1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S3
            [-1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S4
            [-1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S5
            [-1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S6
            [-1, -1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1], # S7
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1, -1, -1], # S8
            [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S9
            [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S10
            [11, 11, 11, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], # S11
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S12
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S13
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S14
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S15
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S16
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S17
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S18
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S19
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S20
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S21
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 23, 24, -1, -1, -1, -1], # S22
            [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23], # S23
            [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25, 24, 24, 24, 24], # S24
            [24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 26, 25, 24, 24, 24, 24], # S25
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S26
        ]
        
        self.estados_aceptacion = {
            1: "ID", 2: "NUMBER", 3: "IGUAL", 4: "NOT", 5: "MENOR", 6: "MAYOR",
            10: "NUMBER", 12: "CADENA", 13: "OPERADOR", 14: "DELIMITADOR",
            15: "IGUALIGUAL", 16: "DIFERENTE", 17: "MENORIGUAL", 18: "MAYORIGUAL",
            19: "AND", 20: "OR", 21: "PUNTO",
            22: "OPERADOR"
        }
        
        self.mapa_operadores = {
            '+': 'MAS', '-': 'MENOS', '*': 'POR', '/': 'DIV', '%': 'MOD',
            '(': 'PARENTESIS_IZQ', ')': 'PARENTESIS_DER', '{': 'LLAVE_IZQ', '}': 'LLAVE_DER',
            '[': 'CORCHETE_IZQ', ']': 'CORCHETE_DER', ';': 'PUNTOCOMA', ',': 'COMA',
        }

    def _obtener_columna(self, caracter):
        if caracter.isalpha() or caracter == '_': return 0 
        if caracter.isdigit(): return 1
        if caracter == '.': return 2
        if caracter == '"': return 3
        if caracter == '=': return 4
        if caracter == '!': return 5
        if caracter == '<': return 6
        if caracter == '>': return 7
        if caracter == '&': return 8
        if caracter == '|': return 9
        if caracter == '/': return 10
        if caracter == '*': return 11
        if caracter in "+-%": return 12
        if caracter in "(){}[]:,;": return 13
        if caracter.isspace(): return 14
        return 15

    def analizar(self, codigo_fuente):
        tokens = []
        linea = 1
        pos = 0
        
        while pos < len(codigo_fuente):
            while pos < len(codigo_fuente) and codigo_fuente[pos].isspace():
                if codigo_fuente[pos] == '\n':
                    linea += 1
                pos += 1
            if pos >= len(codigo_fuente):
                break

            estado_actual = 0
            lexema_actual = ""
            ultimo_estado_aceptacion = -1
            pos_ultimo_aceptacion = -1
            
            temp_pos = pos
            while temp_pos < len(codigo_fuente):
                caracter = codigo_fuente[temp_pos]
                
                # Para el contador de líneas, es mejor manejarlo después de tokenizar.
                
                columna = self._obtener_columna(caracter)
                proximo_estado = self.matriz[estado_actual][columna]

                if estado_actual == 23 and caracter == '\n':
                    proximo_estado = -1 # Forzamos la salida del bucle
                
                if estado_actual == 25 and caracter != '/':
                    proximo_estado = 24
                
                if proximo_estado == -1:
                    break 

                estado_actual = proximo_estado
                lexema_actual += caracter
                
                if estado_actual in self.estados_aceptacion:
                    ultimo_estado_aceptacion = estado_actual
                    pos_ultimo_aceptacion = temp_pos + 1
                
                temp_pos += 1
            
            if estado_actual == 23:
                pos = temp_pos + 1 
                linea += lexema_actual.count('\n') + 1
                continue
            if estado_actual == 26: 
                pos = temp_pos
                linea += lexema_actual.count('\n')
                continue
            
            if estado_actual in [24, 25] and temp_pos >= len(codigo_fuente):
                 tokens.append({'tipo': 'ERROR', 'valor': 'Comentario de bloque no cerrado', 'linea': linea})
                 pos = temp_pos
                 continue

            if estado_actual == 11 and temp_pos >= len(codigo_fuente):
                tokens.append({'tipo': 'ERROR', 'valor': 'Cadena no cerrada', 'linea': linea})
                pos = temp_pos 
                continue

            if ultimo_estado_aceptacion == -1:
                lexema_error = codigo_fuente[pos]
                tokens.append({'tipo': 'ERROR', 'valor': f"Caracter inesperado '{lexema_error}'", 'linea': linea})
                pos += 1
                continue
            
            lexema_final = codigo_fuente[pos:pos_ultimo_aceptacion]
            linea += lexema_final.count('\n') 
            
            tipo_token = self.estados_aceptacion[ultimo_estado_aceptacion]
            
            if tipo_token == "ID" and lexema_final in self.reservadas:
                tipo_token = self.reservadas[lexema_final]
            elif tipo_token == "OPERADOR":
                tipo_token = self.mapa_operadores.get(lexema_final, tipo_token)
            elif tipo_token == "DELIMITADOR":
                tipo_token = self.mapa_operadores.get(lexema_final, tipo_token)

            valor_token = lexema_final.strip('"') if tipo_token == 'CADENA' else lexema_final

            tokens.append({'tipo': tipo_token, 'valor': valor_token.strip(), 'linea': linea})
            
            pos = pos_ultimo_aceptacion
        
        return tokens