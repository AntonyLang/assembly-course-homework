.8086
.model small
.stack 100h
.data
    prompt db 'Please input a Hex number (1..2 digits): $'
    result db 'The Dec number: $'
    buffer db 3, 0, 3 dup(0)
.code
start:
    mov ax, @data
    mov ds, ax
    mov dx, offset prompt
    mov ah, 09h
    int 21h
    mov dx, offset buffer
    mov ah, 0ah
    int 21h
    xor cx, cx
    mov cl, buffer+1
    mov si, offset buffer+2
    xor bx, bx
parse_hex:
    mov al, [si]
    cmp al, '9'
    jbe decimal_digit
    and al, 0dfh            ; a..f -> A..F
    sub al, 'A'-10
    jmp short append_digit
decimal_digit:
    sub al, '0'
append_digit:
    shl bx, 1
    shl bx, 1
    shl bx, 1
    shl bx, 1
    xor ah, ah
    add bx, ax
    inc si
    loop parse_hex
    call print_newline
    mov dx, offset result
    mov ah, 09h
    int 21h
    mov ax, bx
    call print_decimal
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
