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
    mov cx, 2

row_loop:
    push cx                 ; Save outer count
    mov cx, 13

column_loop:
    mov dl, bl
    mov ah, 02h
    int 21h
    inc bl

    cmp cx, 1
    je no_space
    mov dl, ' '
    mov ah, 02h
    int 21h

no_space:
    loop column_loop

    mov dx, offset newline
    mov ah, 09h
    int 21h
    pop cx                  ; Restore outer count
    loop row_loop

    mov ax, 4c00h
    int 21h
end start
