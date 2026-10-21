print_decimal proc near
    push bx
    mov bx, 10
    call print_unsigned
    pop bx
    ret
print_decimal endp

print_hex proc near
    push bx
    mov bx, 16
    call print_unsigned
    pop bx
    ret
print_hex endp

print_unsigned proc near
    push ax
    push cx
    push dx
    xor cx, cx
divide_digit:
    xor dx, dx
    div bx                  ; AX = quotient, DX = remainder
    push dx
    inc cx
    cmp ax, 0
    jne divide_digit
output_digit:
    pop dx
    cmp dl, 9
    jbe numeric_digit
    add dl, 'A'-10
    jmp short emit_digit
numeric_digit:
    add dl, '0'
emit_digit:
    mov ah, 02h
    int 21h
    loop output_digit
    pop dx
    pop cx
    pop ax
    ret
print_unsigned endp

print_newline proc near
    push ax
    push dx
    mov dl, 0dh
    mov ah, 02h
    int 21h
    mov dl, 0ah
    int 21h
    pop dx
    pop ax
    ret
print_newline endp

read_decimal proc near
    mov ah, 0ah
    int 21h
    mov si, dx
    xor cx, cx
    mov cl, [si+1]          ; Input length
    add si, 2
    xor ax, ax
    mov bx, 10
read_digit:
    mul bx
    xor dx, dx
    mov dl, [si]
    sub dl, '0'
    add ax, dx
    inc si
    loop read_digit
    ret
read_decimal endp
