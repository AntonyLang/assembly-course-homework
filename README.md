# 8086 汇编课程作业

本仓库提交汇编课程作业 1、2、3 和进制转换课堂练习，包含带注释源码、可执行文件、实际反汇编、运行输出及复现脚本。

## 作业导航

| 题目 | 完成内容 | 提交入口 |
| --- | --- | --- |
| 作业 1：Hello world | 独立汇编和链接；DEBUG U 查看机器码；DEBUG E 将代码和数据写入内存执行 | [说明、源码和 EXE](homework1/README.md) |
| 作业 2：ASCII 小写字母表 | LOOP 双重循环保存/恢复 CX；条件跳转；C 实现及反汇编中文注释 | [三种实现与验证](homework2/README.md) |
| 作业 3：求和 | 1..100=5050；寄存器/数据段/栈三种保存方式；输入 n；C 实现与反汇编中文注释 | [源码、EXE 与分析](homework3/README.md) |
| 课堂练习：进制转换 | 1～2 位十六进制转十进制；追加十进制转十六进制 | [两种转换与示例](exercises/base-conversion/README.md) |

## 验证结果

已统一编译并运行 **648 个 DOS 用例 + 101 个 C 用例**，全部通过。另验证了空 DEBUG 会话中写内存执行 Hello、独立链接过程，以及 9 个 DOS 程序的反汇编。

- ASCII 三种实现输出逐字节一致：每行 13 个字母，两行 54 字节（含空格及 CR+LF）。
- 三种累计和存储方式均打印 `5050`；汇编和 C 的输入求和均覆盖 n=1..100。
- 十六进制转十进制覆盖 00..FF 的大小写及单字符输入；十进制转十六进制含 0、5050、65535 等边界。

机器可读结果见 [evidence/verification.json](evidence/verification.json)，各汇编程序的编译记录见 [evidence/compilation.txt](evidence/compilation.txt)。各作业目录中的 `.out` 是真实程序输出，`.dis` 是 DOS DEBUG 输出；C 原始反汇编与中文注释分别保存。

## 环境与复现

手写汇编：**8086、16 位 DOS、MASM 兼容语法、INT 21h**。JWasm 汇编，作业 1 另外使用 JWlink 独立链接，DOSBox-X 运行与调试。C 使用 **GCC / Windows x86-64** 编译，GNU objdump 反汇编；与手写 DOS 汇编的目标位数分别注明。

1. 在 64 位 Windows 准备 Python 3.9+ 和 MinGW-w64 GCC、objdump，并将其加入 PATH。无需第三方 Python 包。
2. 下载本仓库，执行 `python scripts/setup_tools.py`。该命令明确下载官方便携工具到 `tools/`，校验文件并用现有 GCC 构建 JWasm64，不修改系统 PATH。
3. 执行 `python scripts/build_all.py`，统一编译、链接、运行验证并更新结果。
4. 双击 [run_homework.cmd](run_homework.cmd) 查看演示，或 [open_environment.cmd](open_environment.cmd) 打开交互 DOS 环境。环境会把 `build/dos` 挂载成 D 盘，可输入 `hello`、`loop`、`jump`、`sumreg`、`sumdata`、`sumstack`、`sumn`、`hex2dec`、`dec2hex`。

已经配置过本项目便携环境的电脑可从第 3 步开始。提交的 DOS EXE 也可在其他兼容 DOS 环境中直接运行，无需重新编译；C EXE 在 Windows 下运行。GitHub 文件页面可用 **Raw / Download raw file** 下载 EXE。

```powershell
python scripts/build_all.py
.\homework2\ascii_c.exe
.\homework3\sum_c.exe
```

源码中的公共十进制输入、十进制/十六进制输出和换行函数位于 [common/dosio.inc](common/dosio.inc)。输入程序按题目约定接受合法输入，具体范围见各作业说明。

## 目录与提交范围

`homework1/`、`homework2/`、`homework3/`、`exercises/` 保存作业，`common/` 保存共享汇编例程，`scripts/` 保存复现入口，`evidence/` 保存统一验证摘要。

工具安装包、本机运行日志、临时文件和课程原始 PDF/截图不提交。EXE 是题目要求的作业产物，保留在版本控制中。工具版本、下载来源与 SHA-256 见 [docs/toolchain.json](docs/toolchain.json)。
