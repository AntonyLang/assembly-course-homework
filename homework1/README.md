# 作业 1：Hello world

## 提交内容

| 文件 | 用途 |
| --- | --- |
| [hello.asm](hello.asm) | MASM 兼容的 8086 汇编源码 |
| [hello.exe](hello.exe) | 先汇编为 OMF OBJ，再独立链接得到的 16 位 DOS EXE |
| [hello.lst](hello.lst) | 地址、机器码与源指令的对应关系 |
| [hello.dis](hello.dis) | DOS DEBUG 的 `u` 反汇编结果 |
| [link.txt](link.txt)、[hello.map](hello.map) | 实际链接输出与地址映射 |
| [memory.dbg](memory.dbg)、[memory_debug.txt](memory_debug.txt) | DEBUG 写内存的输入脚本与实际执行记录 |

## 方式一：源码 → 汇编 → 链接 → 运行

在 DOS 学习环境中执行 `hello`，输出：

```text
Hello world!
```

实际构建分为两个步骤，没有用直接生成 EXE 代替“链接”：

```text
JWasm64 -omf -Fohello.obj hello.asm
JWlinkd format dos file hello.obj name hello.exe option map=hello.map
```

第一个命令在 Windows 下运行；第二个在 DOSBox-X 的 386 配置下运行，因为链接器本身需要 DOS 保护模式。最终 Hello 程序仍是 8086 / 16 位 DOS 程序，统一测试时用 8086 配置执行。根目录的构建脚本自动完成这些步骤。

源码中 `mov ax,@data / mov ds,ax` 初始化数据段；`mov dx,offset message` 把字符串偏移地址放入 DX；`AH=09h / INT 21h` 输出 DS:DX 指向的 `$` 结尾字符串；`AX=4C00h / INT 21h` 正常退出。`0Dh,0Ah` 表示回车换行，`$` 作为结束标志不输出。

在 DOSBox-X 下：

```text
debug hello.exe
u cs:0 10
g
q
```

`u` 后的末地址为十六进制，当前程序代码长度为 11h 字节。实际段值随加载位置变化，应使用 `CS`，不要照抄截图中的段地址。

## 方式二：DEBUG E 直接写代码和数据

在 DOSBox-X 的 D 盘运行：

```text
debug < memory.dbg
```

这是从空 DEBUG 会话开始，**没有加载 hello.exe**。第一条 `e` 把 14 字节机器码写入 `CS:0100`，第二条把字符串写入 `CS:0120`，然后设置 IP 并用 `g=0100` 执行。

| 偏移 | 机器码 | 指令 | 含义 |
| --- | --- | --- | --- |
| 0100 | `0E` | `push cs` | 将当前代码段值压栈 |
| 0101 | `1F` | `pop ds` | DS=CS，使代码和字符串处在同一段 |
| 0102 | `BA 20 01` | `mov dx,0120h` | 指向刚写入的字符串 |
| 0105 | `B4 09` | `mov ah,09h` | 选择字符串输出服务 |
| 0107 | `CD 21` | `int 21h` | 打印字符串 |
| 0109 | `B8 00 4C` | `mov ax,4C00h` | 选择正常退出 |
| 010C | `CD 21` | `int 21h` | 返回 DOS |

`BA 20 01` 中的 16 位立即数为 `0120h`，低字节在前，这是 x86 的小端存储。数据为 `48 65 6C 6C 6F 20 77 6F 72 6C 64 21 0D 0A 24`，对应 `Hello world!`、回车、换行、`$`。

完整的 `e`、`r ip`、`u`、`d`、`g` 命令见输入脚本；实际执行记录同时展示机器码反汇编、内存数据和 `Hello world!`，最后显示 `Program terminated normally (0000)`。
