.8086
.model small
.stack 100h
.data
    prompt db 'Input n (1..100): $'
    result db 'Sum: $'
    buffer db 4, 0, 4 dup(0)
.code
start:
    mov ax, @data
    mov ds, ax
    mov dx, offset prompt
    mov ah, 09h
    int 21h
    mov dx, offset buffer
    call read_decimal
    mov cx, ax
    xor ax, ax
    mov bx, 1
sum_loop:
    add ax, bx
    inc bx
    loop sum_loop
    call print_newline
    push ax                 ; Save sum
    mov dx, offset result
    mov ah, 09h
    int 21h
    pop ax
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
