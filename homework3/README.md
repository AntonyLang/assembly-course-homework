# 作业 3：求和与十进制输出

基本要求：实际累加 `1+2+…+100` 并输出 `5050`；分别尝试寄存器、数据段、栈保存结果；输入 `1..100` 的 n，计算 `1+…+n`；用 C 实现并注释反汇编。

| 实现 | 源码 | EXE | 运行输出 | DEBUG 反汇编 |
| --- | --- | --- | --- | --- |
| 累计和保存在 AX | [sum_reg.asm](sum_reg.asm) | [sumreg.exe](sumreg.exe) | [5050](sumreg.out) | [sumreg.dis](sumreg.dis) |
| 累计和保存在数据段 | [sum_data.asm](sum_data.asm) | [sumdata.exe](sumdata.exe) | [5050](sumdata.out) | [sumdata.dis](sumdata.dis) |
| 累计和保存在栈中 | [sum_stack.asm](sum_stack.asm) | [sumstack.exe](sumstack.exe) | [5050](sumstack.out) | [sumstack.dis](sumstack.dis) |
| 键盘输入 n | [sum_input.asm](sum_input.asm) | [sumn.exe](sumn.exe) | [n=100](sumn.out) | [sumn.dis](sumn.dis) |
| C 语言 | [sum_c.c](sum_c.c) | [sum_c.exe](sum_c.exe) | [n=100](C.OUT) | [原始反汇编](sum_c_disassembly.txt)、[逐条中文注释](sum_c_annotated.txt) |

## 算法和数据范围

固定求和从 0 开始，每次加上 BX 中的数（1 到 100），循环 100 次，得到 5050。没有直接打印预先写好的字符串，也没有用公式代替循环。

5050 超过 8 位无符号数的上限 255，需要至少 16 位。8086 的 AX 和 `DW` 均为 16 位，可表示 0..65535，足够容纳所有合法输入的结果。`n(n+1)/2` 用作验证时的期望值，提交程序实际采用逐项累加。

三个固定版本在每轮循环之间分别将累计和保存在 AX、`total dw 0`、栈顶。栈版本每轮 `pop ax → add ax,bx → push ax`，完成后弹出最终结果；压栈和出栈次数配平，再调用打印函数。

## 输入和数值转换

DOSBox-X 中输入 `sumn`，键入 `1..100` 的十进制整数并回车：

```text
Input n (1..100): 100
Sum: 5050
```

输入使用 `INT 21h / AH=0Ah` 的缓冲区输入功能。缓冲区第一个字节是容量（包含终止回车所需空间），第二个字节是读入的字符数，从第三个字节开始存字符。逐位执行 `value=value*10+(character-'0')`，得到 n。

数值 5050 不能直接当作一个字符输出。公共例程 [dosio.inc](../common/dosio.inc) 反复将 `DX:AX` 除以 10，把余数压栈，再出栈、加 `'0'` 转为字符输出。每次 DIV 前清零 DX，避免把上轮余数带入下一次除法。零也会至少转换一次，输出 `0`。

程序按题目范围接受合法输入；本作业没有扩展为任意文本输入校验系统。所有 n=1..100 已在 DOS 汇编与 C 程序中逐一运行验证。

## C 语言与反汇编

输入 n 后，用 `for(i=1;i<=n;++i)` 累加到 `unsigned int total`。当 n=100 时满足固定求和要求；其余合法 n 满足输入扩展要求。

实际 main 反汇编展示了 `scanf` 写入 n、循环初始化、`CMP/JLE` 判断、`ADD` 累加和 `printf` 输出的完整对应关系。链接时移除含本机路径的调试信息，保留函数符号。本机 GCC 的 C 输出为 Windows x86-64 程序，手写汇编为 16 位 DOS 程序；文件中分别标注了目标与调用约定。
