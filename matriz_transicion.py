# matriz_transicion.py

from tokens import Tokens

class MatrizTransicion:
    def __init__(self):
        self.reservadas = Tokens.reservadas
        
        # ESTADO DE ERROR = -1
        # Columnas: 0=L 1=D, 2=., 3=", 4==, 5=!, 6=<,, 7=>, 8=&, 9=|, 10=OpA, 11=Del, 12=WS, 13=Otro
        self.matriz = [
        #    0   1   2   3   4   5   6   7   8   9  10  11  12  13
            [ 1,  2, 21, 11,  3,  4,  5,  6,  7,  8, 13, 14,  0, -1], # S0: Inicial
            [ 1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S1: En ID
            [-1,  2,  9, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S2: En Número Entero
            [-1, -1, -1, -1, 15, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S3: Vio un =
            [-1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S4: Vio un !
            [-1, -1, -1, -1, 17, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S5: Vio un <
            [-1, -1, -1, -1, 18, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S6: Vio un >
            [-1, -1, -1, -1, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1], # S7: Vio un &
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 20, -1, -1, -1, -1], # S8: Vio un |
            [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S9: Vio un . después de un número
            [-1, 10, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1], # S10: En Número Double
            [11, 11, 11, 12, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11], # S11: En Cadena
            # Estados de aceptación final (no tienen más transiciones)
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S12: CADENA
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S13: Op. Aritméticos
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S14: Delimitadores
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S15: IGUALIGUAL
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S16: DIFERENTE
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S17: MENORIGUAL
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S18: MAYORIGUAL
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S19: AND
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S20: OR
            [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1], # S21: PUNTO
        ]
        
        self.estados_aceptacion = {
            1: "ID", 2: "NUMBER", 3: "IGUAL", 4: "NOT", 5: "MENOR", 6: "MAYOR",
            10: "NUMBER", 12: "CADENA", 13: "OPERADOR", 14: "DELIMITADOR",
            15: "IGUALIGUAL", 16: "DIFERENTE", 17: "MENORIGUAL", 18: "MAYORIGUAL",
            19: "AND", 20: "OR", 21: "PUNTO"
        }
        
        # Mapeo de lexemas a tokens para casos especiales
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
        if caracter in "+-*/%": return 10
        if caracter in "(){}[]:,;": return 11
        if caracter.isspace(): return 12
        return 13

    def analizar(self, codigo_fuente):
        tokens = []
        linea = 1
        pos = 0
        
        while pos < len(codigo_fuente):
            while pos < len(codigo_fuente) and codigo_fuente[pos].isspace():
                if codigo_fuente[pos] == '\n':
                    linea += 1
                pos += 1
                
            
            # Si después de saltar espacios llegamos al final, salimos del bucle principal
            if pos >= len(codigo_fuente):
                break
            estado_actual = 0
            lexema_actual = ""
            ultimo_estado_aceptacion = -1
            pos_ultimo_aceptacion = -1
            
            temp_pos = pos
            while temp_pos < len(codigo_fuente):
                caracter = codigo_fuente[temp_pos]
                if caracter == '\n' and estado_actual == 0:
                    linea += 1

                columna = self._obtener_columna(caracter)
                proximo_estado = self.matriz[estado_actual][columna]

                if proximo_estado == -1:
                    break 

                estado_actual = proximo_estado
                lexema_actual += caracter
                
                if estado_actual in self.estados_aceptacion:
                    ultimo_estado_aceptacion = estado_actual
                    pos_ultimo_aceptacion = temp_pos + 1
                
                temp_pos += 1
            

            if estado_actual == 11 and temp_pos >= len(codigo_fuente):
                tokens.append({'tipo': 'ERROR', 'valor': 'Cadena no cerrada', 'linea': linea})
                pos = temp_pos 
                continue


            if ultimo_estado_aceptacion == -1:
                if not codigo_fuente[pos].isspace():
                    lexema_error = codigo_fuente[pos]
                    tokens.append({'tipo': 'ERROR', 'valor': f"Caracter inesperado '{lexema_error}'", 'linea': linea})
                pos += 1
                continue
            
            lexema_final = codigo_fuente[pos:pos_ultimo_aceptacion]
            tipo_token = self.estados_aceptacion[ultimo_estado_aceptacion]
            
            if tipo_token == "ID" and lexema_final in self.reservadas:
                tipo_token = self.reservadas[lexema_final]
            elif tipo_token == "OPERADOR":
                tipo_token = self.mapa_operadores[lexema_final]
            elif tipo_token == "DELIMITADOR":
                tipo_token = self.mapa_operadores[lexema_final]

            tokens.append({'tipo': tipo_token, 'valor': lexema_final, 'linea': linea})
            
            for char in lexema_final:
                if char == '\n':
                    linea +=1
            pos = pos_ultimo_aceptacion
            
        return tokens