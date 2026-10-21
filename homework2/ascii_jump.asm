.8086
.model small
.stack 100h

.data
    newline db 0dh, 0ah, '$'

.code
start:
    mov ax, @data
    mov ds, ax
    mov bl, 'a'
    mov si, 2

row_loop:
    mov di, 13

column_loop:
    mov dl, bl
    mov ah, 02h
    int 21h
    inc bl

    cmp di, 1
    je no_space
    mov dl, ' '
    mov ah, 02h
    int 21h

no_space:
    dec di
    jnz column_loop

    mov dx, offset newline
    mov ah, 09h
    int 21h
    dec si
    jnz row_loop

    mov ax, 4c00h
    int 21h
end start
