; Keep the running total on the stack between loop iterations.
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
    push ax                 ; Stack starts with the running total 0.
    mov bx, 1
    mov cx, 100
sum_loop:
    pop ax                  ; Take out the previous total.
    add ax, bx
    push ax                 ; Save the new total back on the stack.
    inc bx
    loop sum_loop
    pop ax                  ; Balance the stack before calling output routines.
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
