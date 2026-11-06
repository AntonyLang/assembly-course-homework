.8086
.model small
.stack 100h
.data
table db 7,2,3,4,5,6,7,8,9
      db 2,4,7,8,10,12,14,16,18
      db 3,6,9,12,15,18,21,24,27
      db 4,8,12,16,7,24,28,32,36
      db 5,10,15,20,25,30,35,40,45
      db 6,12,18,24,30,7,42,48,54
      db 7,14,21,28,35,42,49,56,63
      db 8,16,24,32,40,48,56,7,72
      db 9,18,27,36,45,54,63,72,81
heading db 'x y',0dh,0ah,'$'
error_text db ' error',0dh,0ah,'$'
done_text db 'accomplish!',0dh,0ah,'$'
.code
start:
    mov ax,@data
    mov ds,ax
    mov dx,offset heading
    mov ah,09h
    int 21h
    mov si,offset table
    mov bl,1
    mov cx,9
row_loop:
    push cx
    mov bh,1
    mov cx,9
column_loop:
    call check_cell
    inc si
    inc bh
    loop column_loop
    inc bl
    pop cx
    loop row_loop
    mov dx,offset done_text
    mov ah,09h
    int 21h
    mov ax,4c00h
    int 21h

check_cell proc near
    push ax
    push bx
    push cx
    push dx
    push si
    mov al,bl
    mul bh
    cmp al,[si]
    je cell_done
    xor ax,ax
    mov al,bl
    call print_decimal
    mov dl,' '
    mov ah,02h
    int 21h
    xor ax,ax
    mov al,bh
    call print_decimal
    mov dx,offset error_text
    mov ah,09h
    int 21h
cell_done:
    pop si
    pop dx
    pop cx
    pop bx
    pop ax
    ret
check_cell endp
include dosio.inc
end start
