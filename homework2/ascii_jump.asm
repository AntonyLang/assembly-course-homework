; Homework 2 (2): the same output, using conditional jumps, without LOOP.
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
    mov si, 2               ; SI counts rows; DI counts columns independently.

row_loop:
    mov di, 13

column_loop:
    mov dl, bl
    mov ah, 02h
    int 21h
    inc bl

    cmp di, 1
    je no_space             ; ZF=1 when this is the last column.
    mov dl, ' '
    mov ah, 02h
    int 21h

no_space:
    dec di                  ; Unlike LOOP, DEC updates ZF.
    jnz column_loop         ; ZF=0 means there are more letters in this row.

    mov dx, offset newline
    mov ah, 09h
    int 21h
    dec si
    jnz row_loop            ; Continue until both rows have been printed.

    mov ax, 4c00h
    int 21h
end start
