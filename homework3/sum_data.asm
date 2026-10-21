; Keep the running total in a word in the data segment.
.8086
.model small
.stack 100h
.data
    total dw 0
.code
start:
    mov ax, @data
    mov ds, ax
    mov bx, 1
    mov cx, 100
sum_loop:
    add total, bx
    inc bx
    loop sum_loop
    mov ax, total
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
