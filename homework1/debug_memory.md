# DEBUG 写内存运行 Hello world

在 DOS 环境输入 `debug`，执行：

```text
e cs:0100 0e 1f ba 20 01 b4 09 cd 21 b8 00 4c cd 21
e cs:0120 48 65 6c 6c 6f 20 77 6f 72 6c 64 21 0d 0a 24
r ip
0100
u cs:0100 010d
d cs:0120 012e
g=0100
q
```

第一条 `e` 在 `CS:0100` 写入代码，对应：

```asm
push cs
pop ds
mov dx,0120h
mov ah,09h
int 21h
mov ax,4c00h
int 21h
```

第二条 `e` 在 `CS:0120` 写入 `Hello world!`、回车、换行和结束符 `$`。`push cs / pop ds` 令 DS=CS，使 DS:DX 指向该字符串。

`u` 查看指令，`d` 查看数据，`g=0100` 从代码起始地址运行，屏幕输出 `Hello world!`。这里使用当前 CS，不依赖固定的段地址。
