; --- GENERADO POR TU COMPILADOR ---
section .data
    newline db 10, 0

section .bss
    buffer resb 24
    align 8
var_a: resq 1

section .text
global _start
_start:
    mov rax, 20
    mov [var_a], rax
    mov rax, [var_a]
    push rax
    pop rax
    call print_number
    call print_newline

    ; Exit
    mov rax, 60
    mov rdi, 0
    syscall

print_newline:
    mov rax, 1
    mov rdi, 1
    mov rsi, newline
    mov rdx, 1
    syscall
    ret

print_string:
    mov rsi, rax
    mov rdx, 0
.find_len:
    cmp byte [rsi+rdx], 0
    je .print_now
    inc rdx
    jmp .find_len
.print_now:
    mov rax, 1
    mov rdi, 1
    syscall
    ret

print_number:
    push rbx
    mov rcx, buffer
    add rcx, 23
    mov byte [rcx], 0
    mov rbx, 10
.next_digit:
    dec rcx
    xor rdx, rdx
    div rbx
    add dl, '0'
    mov [rcx], dl
    test rax, rax
    jnz .next_digit
    mov rsi, rcx
    mov rdx, buffer
    add rdx, 23
    sub rdx, rcx
    mov rax, 1
    mov rdi, 1
    syscall
    pop rbx
    ret