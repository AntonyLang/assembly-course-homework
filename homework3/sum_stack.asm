.8086
.model small
.stack 100h
.data
    unused db 0
.code
start:
    mov ax, @data
    mov ds, ax
    xor ax, ax
    push ax                 ; Store sum on stack
    mov bx, 1
    mov cx, 100
sum_loop:
    pop ax
    add ax, bx
    push ax                 ; Store sum on stack
    inc bx
    loop sum_loop
    pop ax
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
