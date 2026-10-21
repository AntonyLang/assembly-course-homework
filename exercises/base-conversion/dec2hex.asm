; Extra task: unsigned decimal 0..65535 -> uppercase hexadecimal.
.8086
.model small
.stack 100h
.data
    prompt db 'Please input a Dec number (0..65535): $'
    result db 'The Hex number: $'
    buffer db 6, 0, 6 dup(0)
.code
start:
    mov ax, @data
    mov ds, ax
    mov dx, offset prompt
    mov ah, 09h
    int 21h
    mov dx, offset buffer
    call read_decimal
    call print_newline
    push ax
    mov dx, offset result
    mov ah, 09h
    int 21h
    pop ax
    call print_hex
    call print_newline
    mov ax, 4c00h
    int 21h
include dosio.inc
end start
