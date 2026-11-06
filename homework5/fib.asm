.8086
.model small
.stack 1000h
.data
prompt db 'Input n (1..100): $'
result db 'F(n): $'
buffer db 4,0,4 dup(0)
ready db 1,1,99 dup(0)
cache dw 5 dup(0),1,4 dup(0),495 dup(0)
number dw 5 dup(0)
.code
start:
    mov ax,@data
    mov ds,ax
    mov dx,offset prompt
    mov ah,09h
    int 21h
    mov dx,offset buffer
    call read_decimal
    mov di,ax
    call print_newline
    mov dx,offset result
    mov ah,09h
    int 21h
    call fib
    call print_big
    call print_newline
    mov ax,4c00h
    int 21h

; DI=n; result (low to high): AX,BX,CX,DX,SI. Preserve DI and BP.
fib proc near
    push bp
    push di
    cmp ready[di],0
    jne cached
    dec di
    call fib
    push si
    push dx
    push cx
    push bx
    push ax
    dec di
    call fib
    pop bp
    add ax,bp
    pop bp
    adc bx,bp
    pop bp
    adc cx,bp
    pop bp
    adc dx,bp
    pop bp
    adc si,bp
    inc di
    inc di
    mov bp,di
    shl bp,1
    shl bp,1
    shl bp,1
    add bp,di
    add bp,di
    mov ds:cache[bp],ax
    mov ds:cache[bp+2],bx
    mov ds:cache[bp+4],cx
    mov ds:cache[bp+6],dx
    mov ds:cache[bp+8],si
    mov ready[di],1
    jmp short fib_done
cached:
    mov bp,di
    shl bp,1
    shl bp,1
    shl bp,1
    add bp,di
    add bp,di
    mov ax,ds:cache[bp]
    mov bx,ds:cache[bp+2]
    mov cx,ds:cache[bp+4]
    mov dx,ds:cache[bp+6]
    mov si,ds:cache[bp+8]
fib_done:
    pop di
    pop bp
    ret
fib endp

print_big proc near
    mov number,ax
    mov number+2,bx
    mov number+4,cx
    mov number+6,dx
    mov number+8,si
    xor di,di
next_digit:
    mov si,8
    mov cx,5
    xor dx,dx
    mov bx,10
divide_word:
    mov ax,number[si]
    div bx
    mov number[si],ax
    sub si,2
    loop divide_word
    push dx
    inc di
    mov ax,number
    or ax,number+2
    or ax,number+4
    or ax,number+6
    or ax,number+8
    jnz next_digit
write_digit:
    pop dx
    add dl,'0'
    mov ah,02h
    int 21h
    dec di
    jnz write_digit
    ret
print_big endp
include dosio.inc
end start
