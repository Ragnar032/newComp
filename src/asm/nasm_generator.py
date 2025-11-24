# src/asm/nasm_generator.py

class NasmGenerator:
    def __init__(self):
        self.asm_lines = []
        self.variables = set()
        self.strings = {} 
        self.string_counter = 0
        self.last_push_type = 'NUM'
        
        # Mapeo de Operadores a Instrucciones NASM
        self.op_map = {
            '+':  ['    pop rbx', '    pop rax', '    add rax, rbx', '    push rax'],
            '-':  ['    pop rbx', '    pop rax', '    sub rax, rbx', '    push rax'],
            '*':  ['    pop rbx', '    pop rax', '    imul rax, rbx', '    push rax'],
            '/':  ['    pop rbx', '    pop rax', '    cqo', '    idiv rbx', '    push rax'],
            '==': ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    sete al', '    movzx rax, al', '    push rax'],
            '!=': ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    setne al', '    movzx rax, al', '    push rax'],
            '>':  ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    setg al', '    movzx rax, al', '    push rax'],
            '<':  ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    setl al', '    movzx rax, al', '    push rax'],
            '>=': ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    setge al', '    movzx rax, al', '    push rax'],
            '<=': ['    pop rbx', '    pop rax', '    cmp rax, rbx', '    setle al', '    movzx rax, al', '    push rax'],
        }

    def generate(self, quadruples):
        """ Recibe lista de cuádruplos y genera ASM """
        # Paso 1: Escanear variables (ahora desde cuádruplos es más fácil)
        # Si recibes el string postfijo viejo, mantenemos la lógica de split
        # Pero asumiré que sigues usando la lista de cuádruplos como en el último main.
        
        # NOTA: Para compatibilidad con tu Main actual que pasa una lista de dicts:
        if isinstance(quadruples, list):
            self._scan_symbols_from_quads(quadruples)
        else:
            # Si por alguna razón pasas texto plano
            lines = quadruples.strip().split('\n')
            self._scan_symbols(lines)

        self.asm_lines = []
        self._write_header()
        self._write_data_section()
        self._write_bss_section()
        
        # Procesar instrucciones
        self.asm_lines.append("section .text")
        self.asm_lines.append("global _start")
        self.asm_lines.append("_start:")
        
        if isinstance(quadruples, list):
            for quad in quadruples:
                self._process_quadruple(quad)
        else:
            # Fallback para texto plano si cambias el main
            self._write_text_section(quadruples.strip().split('\n'))

        # Salida del programa
        self.asm_lines.append("")
        self.asm_lines.append("    ; Exit")
        self.asm_lines.append("    mov rax, 60")
        self.asm_lines.append("    mov rdi, 0")
        self.asm_lines.append("    syscall")

        self._write_subroutines()
        
        return "\n".join(self.asm_lines)

    def _scan_symbols_from_quads(self, quads):
        for q in quads:
            # Buscar strings en arg1
            if q['arg1'] and str(q['arg1']).startswith('"'):
                content = str(q['arg1']).strip('"')
                if content not in self.strings:
                    self.strings[content] = f"str_{self.string_counter}"
                    self.string_counter += 1
            
            # Buscar variables en res (asignaciones)
            if q['res'] and not q['res'].startswith('T') and not q['res'].startswith('L'):
                self.variables.add(q['res'])

    def _scan_symbols(self, lines):
        # Método legacy por si usas postfijo plano
        for line in lines:
            line = line.strip()
            if not line or line.endswith(':'): continue
            tokens = self._tokenize(line)
            if len(tokens) > 0 and tokens[-1] == '=': self.variables.add(tokens[0])
            for token in tokens:
                if token.startswith('"'):
                    content = token.strip('"')
                    if content not in self.strings:
                        self.strings[content] = f"str_{self.string_counter}"
                        self.string_counter += 1
                elif not token.replace('.', '', 1).isdigit() and token not in self.op_map and token not in ['=', 'PRINT', 'GOTO', 'JUMP_IF_FALSE'] and not token.startswith('L') and token not in ['true', 'false']:
                     self.variables.add(token)

    def _process_quadruple(self, quad):
        op = str(quad['op'])
        arg1 = str(quad['arg1']) if quad['arg1'] is not None else None
        arg2 = str(quad['arg2']) if quad['arg2'] is not None else None
        res = str(quad['res']) if quad['res'] is not None else None

        if op == 'LABEL':
            self.asm_lines.append(f"{res}:")
            return

        # --- ASIGNACIÓN (=) ---
        if op == '=':
            # Si es temporal (T1), asumimos que ya está en la pila o en un registro?
            # En tu modelo actual, los temporales se resuelven antes.
            # Si arg1 es numero
            if arg1.replace('.', '', 1).isdigit():
                self.asm_lines.append(f"    mov rax, {arg1}")
            elif arg1.startswith('T'):
                # Si viene de un temporal, asumimos que el valor quedó en RAX de la operación anterior
                # O si implementas memoria para temporales: mov rax, [var_T1]
                # Para simplificar, si es T, no hacemos mov, confiamos en RAX.
                pass 
            else:
                # Es variable
                self.asm_lines.append(f"    mov rax, [var_{arg1}]")
            
            self.asm_lines.append(f"    mov [var_{res}], rax")

        # --- OPERACIONES ARITMÉTICAS ---
        elif op in self.op_map:
            # Los cuádruplos tienen: +, arg1, arg2, res
            # Necesitamos cargar arg1 y arg2
            
            # Cargar Arg1
            if arg1.replace('.', '', 1).isdigit():
                self.asm_lines.append(f"    mov rax, {arg1}")
                self.asm_lines.append("    push rax")
            else:
                # Variable o Temporal (Asumiendo variable por ahora)
                self.asm_lines.append(f"    mov rax, [var_{arg1}]")
                self.asm_lines.append("    push rax")

            # Cargar Arg2
            if arg2.replace('.', '', 1).isdigit():
                self.asm_lines.append(f"    mov rax, {arg2}")
                self.asm_lines.append("    push rax")
            else:
                self.asm_lines.append(f"    mov rax, [var_{arg2}]")
                self.asm_lines.append("    push rax")

            # Ejecutar operación (usando tu mapa de pila)
            self.asm_lines.extend(self.op_map[op])
            
            # El resultado quedó en la pila (push rax). Lo sacamos y guardamos en RES (Temporal)
            self.asm_lines.append("    pop rax")
            # Aquí definimos el temporal en memoria para usarlo luego
            if res not in self.variables:
                self.asm_lines.append(f"    ; Temporal {res} en RAX")
                # Hack para temporales: usaremos var_T1 en bss si lo agregamos a variables
                # O simplemente lo dejamos en RAX si la siguiente instrucción lo usa inmediatamente (riesgoso)
                # Lo ideal: Guardar en variable temporal.
                self.variables.add(res) # Lo agregamos dinámicamente
                self.asm_lines.append(f"    mov [var_{res}], rax")
            else:
                self.asm_lines.append(f"    mov [var_{res}], rax")

        # --- PRINT ---
        elif op == 'PRINT':
            if arg1.startswith('"'):
                content = arg1.strip('"')
                label = self.strings[content]
                self.asm_lines.append(f"    lea rax, [{label}]")
                self.asm_lines.append("    push rax")
                self.asm_lines.append("    pop rax")
                self.asm_lines.append("    call print_string")
            else:
                if arg1.replace('.', '', 1).isdigit():
                    self.asm_lines.append(f"    mov rax, {arg1}")
                else:
                    self.asm_lines.append(f"    mov rax, [var_{arg1}]")
                self.asm_lines.append("    push rax")
                self.asm_lines.append("    pop rax")
                self.asm_lines.append("    call print_number")
            self.asm_lines.append("    call print_newline")

        # --- GOTO ---
        elif op == 'GOTO':
            self.asm_lines.append(f"    jmp {res}")

        # --- JUMP_IF_FALSE ---
        elif op == 'JUMP_IF_FALSE':
            # arg1 tiene la condición (variable o temporal)
            self.asm_lines.append(f"    mov rax, [var_{arg1}]")
            self.asm_lines.append("    cmp rax, 0")
            self.asm_lines.append(f"    je {res}")

    def _write_header(self):
        self.asm_lines.append("; --- GENERADO POR TU COMPILADOR ---")

    def _write_data_section(self):
        self.asm_lines.append("section .data")
        self.asm_lines.append("    newline db 10, 0") # CAMBIO 1: NULL TERMINATOR
        for content, label in self.strings.items():
            self.asm_lines.append(f'{label}: db "{content}", 0')
        self.asm_lines.append("")

    def _write_bss_section(self):
        self.asm_lines.append("section .bss")
        self.asm_lines.append("    buffer resb 24") # CAMBIO 2: BUFFER 24
        self.asm_lines.append("    align 8")        # CAMBIO 3: ALINEACIÓN
        
        for var in self.variables:
            # Limpieza de seguridad
            if var in self.op_map: continue
            self.asm_lines.append(f'var_{var}: resq 1') 
        self.asm_lines.append("")

    # Método legacy para Postfijo (si se usa)
    def _write_text_section(self, lines):
        self.asm_lines.append("section .text")
        self.asm_lines.append("global _start")
        self.asm_lines.append("_start:")
        
        for line in lines:
            line = line.strip()
            if not line: continue
            if line.endswith(':'):
                self.asm_lines.append(f"{line}")
                continue
            
            tokens = self._tokenize(line)
            is_assignment = (tokens[-1] == '=')
            target_var = tokens[0] if is_assignment else None
            
            for i, token in enumerate(tokens):
                if is_assignment and i == 0: continue
                
                if token == '=':
                    self.asm_lines.append("    pop rax")
                    self.asm_lines.append(f"    mov [var_{target_var}], rax")
                
                elif token in self.op_map:
                    self.asm_lines.extend(self.op_map[token])
                
                elif token == 'PRINT':
                    self.asm_lines.append("    pop rax")
                    if self.last_push_type == 'STR':
                        self.asm_lines.append("    call print_string")
                    else:
                        self.asm_lines.append("    call print_number")
                    self.asm_lines.append("    call print_newline")
                
                elif token == 'GOTO':
                    label = tokens[i-1]
                    self.asm_lines.append(f"    jmp {label}")
                
                elif token == 'JUMP_IF_FALSE':
                    label = tokens[i-1]
                    self.asm_lines.append("    pop rax")
                    self.asm_lines.append("    cmp rax, 0")
                    self.asm_lines.append(f"    je {label}")
                
                elif token.replace('.', '', 1).isdigit():
                    self.asm_lines.append(f"    mov rax, {token}")
                    self.asm_lines.append("    push rax")
                    self.last_push_type = 'NUM'
                
                elif token.startswith('"'):
                    content = token.strip('"')
                    label = self.strings[content]
                    self.asm_lines.append(f"    lea rax, [{label}]")
                    self.asm_lines.append("    push rax")
                    self.last_push_type = 'STR'
                elif token.startswith('L') and token[1:].isdigit():
                    pass
                else:
                    self.asm_lines.append(f"    mov rax, [var_{token}]")
                    self.asm_lines.append("    push rax")
                    self.last_push_type = 'NUM'

    def _write_subroutines(self):
        self.asm_lines.append("")
        self.asm_lines.append("print_newline:")
        self.asm_lines.append("    mov rax, 1")
        self.asm_lines.append("    mov rdi, 1")
        self.asm_lines.append("    mov rsi, newline")
        self.asm_lines.append("    mov rdx, 1")
        self.asm_lines.append("    syscall")
        self.asm_lines.append("    ret")
        
        self.asm_lines.append("")
        self.asm_lines.append("print_string:")
        self.asm_lines.append("    mov rsi, rax")
        self.asm_lines.append("    mov rdx, 0")
        self.asm_lines.append(".find_len:")
        self.asm_lines.append("    cmp byte [rsi+rdx], 0")
        self.asm_lines.append("    je .print_now")
        self.asm_lines.append("    inc rdx")
        self.asm_lines.append("    jmp .find_len")
        self.asm_lines.append(".print_now:")
        self.asm_lines.append("    mov rax, 1")
        self.asm_lines.append("    mov rdi, 1")
        self.asm_lines.append("    syscall")
        self.asm_lines.append("    ret")

        self.asm_lines.append("")
        self.asm_lines.append("print_number:")
        self.asm_lines.append("    push rbx") # CAMBIO 4: Guardar registro
        self.asm_lines.append("    mov rcx, buffer")
        self.asm_lines.append("    add rcx, 23") # CAMBIO 5: Offset ajustado
        self.asm_lines.append("    mov byte [rcx], 0")
        self.asm_lines.append("    mov rbx, 10")
        self.asm_lines.append(".next_digit:")
        self.asm_lines.append("    dec rcx")
        self.asm_lines.append("    xor rdx, rdx")
        self.asm_lines.append("    div rbx")
        self.asm_lines.append("    add dl, '0'")
        self.asm_lines.append("    mov [rcx], dl")
        self.asm_lines.append("    test rax, rax")
        self.asm_lines.append("    jnz .next_digit")
        self.asm_lines.append("    mov rsi, rcx")
        self.asm_lines.append("    mov rdx, buffer")
        self.asm_lines.append("    add rdx, 23") # CAMBIO 5: Offset ajustado
        self.asm_lines.append("    sub rdx, rcx")
        self.asm_lines.append("    mov rax, 1")
        self.asm_lines.append("    mov rdi, 1")
        self.asm_lines.append("    syscall")
        self.asm_lines.append("    pop rbx") # CAMBIO 4: Restaurar registro
        self.asm_lines.append("    ret")

    def _tokenize(self, line):
        tokens = []
        token_actual = ""
        dentro_comillas = False
        for char in line:
            if char == '"':
                dentro_comillas = not dentro_comillas
                token_actual += char
            elif char == ' ' and not dentro_comillas:
                if token_actual:
                    tokens.append(token_actual)
                    token_actual = ""
            else:
                token_actual += char
        if token_actual: tokens.append(token_actual)
        return tokens