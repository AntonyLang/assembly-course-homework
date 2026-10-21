# 作业 2：每行打印 13 个小写字母

```text
a b c d e f g h i j k l m
n o p q r s t u v w x y z
```

| 要求 | 源码 | 可执行文件 | 说明及证据 |
| --- | --- | --- | --- |
| 用 LOOP 实现 | [ascii_loop.asm](ascii_loop.asm) | [loop.exe](loop.exe) | [列表文件](loop.lst)、[DEBUG 反汇编](LOOP.DIS)、[输出](LOOP.OUT) |
| 用条件跳转实现 | [ascii_jump.asm](ascii_jump.asm) | [jump.exe](jump.exe) | [列表文件](jump.lst)、[DEBUG 反汇编](JUMP.DIS)、[输出](JUMP.OUT) |
| 用 C 实现并注释反汇编 | [ascii_c.c](ascii_c.c) | [ascii_c.exe](ascii_c.exe) | [原始反汇编](ascii_c_disassembly.txt)、[逐条中文注释](ascii_c_annotated.txt)、[输出](C.OUT) |

## LOOP 与 CX 的保存恢复

外层重复 2 行，内层每行重复 13 次。两条 LOOP 都依赖 CX，所以进入内层前 `push cx` 保存外层计数，内层结束后 `pop cx` 恢复外层计数，再执行外层 LOOP。

第一行：保存 CX=2 → 内层 CX 从 13 减到 0 → 恢复 CX=2 → 外层 LOOP 减到 1。第二行同理，外层 CX 最后减到 0，结束循环。不能直接让内层结束后的 CX=0 进入外层 LOOP，否则它会先减为 FFFFh，产生错误的重复。

BL 保存当前字母，从 ASCII `61h`（a）开始，每次输出后递增，第二行自然从 n 继续。DL 仅作为输出参数，因此输出空格不会破坏 BL 中的字母。`cmp cx,1 / je` 仅控制是否输出空格；重复次数由两层 LOOP 控制。每行最后不留尾空格，使用 CR+LF 换行。

## 条件跳转版本

SI 保存剩余行数，DI 保存当前行剩余字母数；用 `dec di / jnz` 和 `dec si / jnz` 控制两层循环，不使用 LOOP。

LOOP 根据 CX 的值决定跳转且不修改标志；DEC 设置 ZF 等标志，JNZ 判断 ZF 是否为零，因此 DEC 与相应 JNZ 紧接。

## C 与反汇编

C 版本使用两个 for 循环。编译选项为 `-O0 -g -fno-builtin -fno-inline -Wall -Wextra -Wpedantic -std=c90`，以便观察初始化、比较、跳转与自增的对应关系。链接时添加 `-Wl,--strip-debug` 移除包含本机路径的调试信息，保留反汇编所需的函数符号。

本机 C 编译器生成 Windows x86-64 程序，`putchar` 通过 ECX 传参；两份手写汇编生成 16 位 DOS 程序，通过 `AH=02h / INT 21h` 输出。位数及调用方式不同，输出要求相同。逐条注释来自实际 EXE 的 objdump 结果，并核对了机器码与地址。
