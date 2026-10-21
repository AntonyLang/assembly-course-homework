# 课堂练习：进制转换

| 要求 | 源码 | EXE | 实际输出 | DEBUG 反汇编 |
| --- | --- | --- | --- | --- |
| 输入 1～2 位十六进制，输出十进制 | [hex2dec.asm](hex2dec.asm) | [hex2dec.exe](hex2dec.exe) | [ff → 255](hex2dec.out) | [hex2dec.dis](hex2dec.dis) |
| 追加：十进制转十六进制 | [dec2hex.asm](dec2hex.asm) | [dec2hex.exe](dec2hex.exe) | [65535 → FFFF](dec2hex.out) | [dec2hex.dis](dec2hex.dis) |

在 DOSBox-X 中运行 `hex2dec` 或 `dec2hex`，按提示输入并回车。

```text
Please input a Hex number (1..2 digits): ff
The Dec number: 255
```

```text
Please input a Dec number (0..65535): 5050
The Hex number: 13BA
```

## 十六进制 → 十进制

合法输入范围为 `0..FF`，1 或 2 位，不带 `0x` 或 `h` 后缀，接受大小写。`AH=0Ah / INT 21h` 读取字符，数字字符减去 `'0'`，字母统一大写后减去 `'A'` 再加 10。

例如 `ff`：先读 f 得到 15；再读 f，执行 `15*16+15=255`。数值保存在 BX。8086 下使用四次 `shl bx,1` 实现乘 16，而非使用原始 8086 不支持的立即数移位 4。转换后调用公共十进制输出例程。

## 十进制 → 十六进制

追加要求的输入范围选定为无符号 16 位 `0..65535`。逐位十进制解析后，反复除以 16，余数 0..9 映射为 `0..9`，10..15 映射为 `A..F`。余数压栈再逆序弹出，去掉多余前导零，数值零仍输出 `0`。

## 验证

十六进制输入覆盖 `00..FF` 全部 256 个数的大小写形式，以及 `0..f` 单位输入。十进制追加要求验证零、十进制/十六进制边界、5050、32767、32768 和 65535。详细用例数量见根目录 [验证报告](../../evidence/verification.json)。程序使用题目范围内的合法输入。
