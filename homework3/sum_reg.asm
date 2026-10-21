; Basic sum 1..100. Keep the running total in register AX.
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
    mov bx, 1
    mov cx, 100
sum_loop:
    add ax, bx
    inc bx
    loop sum_loop
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
