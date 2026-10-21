; Homework 2 (1): print a-z, 13 letters per line, using nested LOOP.
; MASM-compatible 8086 DOS source. Comments are ASCII for old assemblers.
.8086
.model small
.stack 100h

.data
    newline db 0dh, 0ah, '$'

.code
start:
    mov ax, @data
    mov ds, ax              ; AH=09h requires DS:DX to address the string.
    mov bl, 'a'             ; BL keeps the next letter across space/newline output.
    mov cx, 2               ; Outer loop: two rows.

row_loop:
    push cx                 ; Save outer CX BEFORE starting the inner loop.
    mov cx, 13              ; Inner loop: thirteen letters.

column_loop:
    mov dl, bl
    mov ah, 02h             ; DOS function 02h: output the character in DL.
    int 21h
    inc bl                  ; Advance from a through z; do not restart each row.

    cmp cx, 1
    je no_space             ; Do not append a space after the last letter.
    mov dl, ' '
    mov ah, 02h
    int 21h

no_space:
    loop column_loop        ; CX = CX - 1; jump if CX != 0 (flags unchanged).

    mov dx, offset newline
    mov ah, 09h             ; Output CR, LF; '$' terminates the string.
    int 21h
    pop cx                  ; Restore outer CX after the inner loop exhausted it.
    loop row_loop           ; Outer CX: 2 -> 1 -> 0.

    mov ax, 4c00h           ; DOS function 4Ch: exit with status 0.
    int 21h
end start
