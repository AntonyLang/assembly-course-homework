"""Compile every assignment, then verify the actual DOS and Windows programs."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "build" / "dos"
JWASM = ROOT / "tools" / "jwasm" / "JWasm64.exe"
DOSBOX = ROOT / "tools" / "dosbox-x" / "mingw-build" / "mingw-sdl2" / "dosbox-x.exe"
GCC = shutil.which("gcc")
OBJDUMP = shutil.which("objdump")
ASCII = b"a b c d e f g h i j k l m\r\nn o p q r s t u v w x y z\r\n"
PROGRAMS = [
    ("homework1", "hello.asm", "hello"),
    ("homework2", "ascii_loop.asm", "loop"),
    ("homework2", "ascii_jump.asm", "jump"),
    ("homework3", "sum_reg.asm", "sumreg"),
    ("homework3", "sum_data.asm", "sumdata"),
    ("homework3", "sum_stack.asm", "sumstack"),
    ("homework3", "sum_input.asm", "sumn"),
    ("exercises/base-conversion", "hex2dec.asm", "hex2dec"),
    ("exercises/base-conversion", "dec2hex.asm", "dec2hex"),
]


def run(args, cwd=WORK, **kwargs):
    return subprocess.run([str(x) for x in args], cwd=cwd, check=True,
                          capture_output=True, timeout=180, **kwargs)


def dos_text(path, content):
    path.write_bytes(content.replace("\r\n", "\n").replace("\n", "\r\n").encode("ascii"))


def dos_session(batch, cpu="8086"):
    config = (ROOT / "homework2" / "dosbox-x.conf").read_text(encoding="ascii")
    config = config.replace("cputype=8086", f"cputype={cpu}")
    if cpu != "8086":
        config = config.replace("memsize=1", "memsize=16").replace("xms=false", "xms=true")
        config = config.replace("cycles=fixed 3000", "cycles=fixed 30000")
    dos_text(WORK / "session.conf", config + f"\n{batch}\n")
    result = run([DOSBOX, "-conf", "session.conf", "-nopromptfolder", "-fastlaunch", "-silent"])
    (WORK / "session.log").write_bytes(result.stdout + result.stderr)


def instructions(text):
    result = []
    for line in text.splitlines():
        line = line.split(";", 1)[0].split("#", 1)[0].strip()
        match = re.match(r"([0-9a-f]+):\s*((?:[0-9a-f]{2}\s+)+)(.*?)\s*$", line)
        if match:
            result.append((match.group(1), "".join(match.group(2).split()),
                           " ".join(match.group(3).split())))
    return result


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    print("Compiling all 8086 assembly sources...", flush=True)
    shutil.copyfile(ROOT / "common" / "dosio.inc", WORK / "dosio.inc")
    build_logs = []
    for folder, source, name in PROGRAMS:
        shutil.copyfile(ROOT / folder / source, WORK / source)
        args = [JWASM, "-W3", "-I.", f"-Fl{name}.lst"]
        if name == "hello":
            args += ["-omf", "-Fohello.obj"]
        else:
            args += ["-mz", f"-Fo{name}.exe"]
        result = run(args + [source])
        build_logs.append(result.stdout.decode(errors="replace").replace("\r\n", "\n"))
        listing = (WORK / f"{name}.lst").read_text(encoding="ascii")
        match = re.search(r"^_TEXT\s+.*?16 Bit\s+([0-9A-F]+)", listing, re.MULTILINE)
        code_end = int(match.group(1), 16) - 1
        dos_text(WORK / f"{name}.dbg", f"u cs:0 {code_end:x}\nq\n")
    (evidence / "compilation.txt").write_text("\n".join(build_logs), encoding="utf-8")

    print("Linking homework 1 OMF object with DOS JWlink...", flush=True)
    for src, dest in (("JWlinkd.exe", "linkd.exe"), ("hdpmi32.exe", "hdpmi32.exe")):
        shutil.copyfile(ROOT / "tools" / "jwlink-dos" / src, WORK / dest)
    dos_text(WORK / "linkjob.bat", """@echo off
linkd format dos file hello.obj name hello.exe option map=hello.map > link.log
if errorlevel 1 goto failed
echo PASS>link.ok
exit
:failed
echo FAIL>link.ok
exit
""")
    dos_session("linkjob.bat", cpu="386")
    assert (WORK / "link.ok").read_text().strip() == "PASS", (WORK / "link.log").read_text()

    print("Compiling both C programs and extracting actual disassembly...", flush=True)
    c_outputs = {}
    for folder, source, name in (("homework2", "ascii_c.c", "ascii_c"),
                                  ("homework3", "sum_c.c", "sum_c")):
        directory = ROOT / folder
        result = run([GCC, "-O0", "-g", "-fno-builtin", "-fno-inline", "-Wall", "-Wextra",
                      "-Wpedantic", "-std=c90", "-Wl,--strip-debug", source, "-o", f"{name}.exe"], cwd=directory)
        assert not result.stderr, result.stderr.decode()
        dis = run([OBJDUMP, "-d", "-M", "intel", "--disassemble=main", f"{name}.exe"], cwd=directory)
        (directory / f"{name}_disassembly.txt").write_bytes(dis.stdout)
        # Notes are concrete evidence for this compiler output, not invented pseudocode.
        notes = (directory / f"{name}_annotated.txt").read_text(encoding="utf-8")
        assert instructions(dis.stdout.decode()) == instructions(notes), f"Recheck annotations: {name}"
        if name == "ascii_c":
            c_outputs[name] = run([directory / f"{name}.exe"]).stdout
            assert c_outputs[name] == ASCII
            (directory / "C.OUT").write_bytes(c_outputs[name])
        else:
            for n in range(1, 101):
                output = run([directory / f"{name}.exe"], input=f"{n}\n".encode()).stdout
                assert output.endswith(f"Sum: {n*(n+1)//2}\r\n".encode()), (n, output)
            (directory / "C.OUT").write_bytes(output)

    print("Running unified DOS tests (all hex bytes and all n in 1..100)...", flush=True)
    tests = []
    for name, expected in (("hello", b"Hello world!\r\n"), ("loop", ASCII), ("jump", ASCII),
                           ("sumreg", b"5050\r\n"), ("sumdata", b"5050\r\n"), ("sumstack", b"5050\r\n")):
        tests.append((name, name, None, expected, None))
    # All values 00..FF in both cases; also exercise single-digit input.
    for n in range(256):
        for prefix, value in (("h", f"{n:02x}"), ("u", f"{n:02X}")):
            tests.append((f"{prefix}{n:03}", "hex2dec", value, f"{n}\r\n".encode(), b"The Dec number: "))
    for n in range(16):
        tests.append((f"one{n:02}", "hex2dec", f"{n:x}", f"{n}\r\n".encode(), b"The Dec number: "))
    decimals = [0, 1, 9, 10, 15, 16, 99, 100, 255, 256, 5050, 32767, 32768, 65535]
    for n in decimals:
        tests.append((f"d{n:05}", "dec2hex", str(n), f"{n:X}\r\n".encode(), b"The Hex number: "))
    for n in range(1, 101):
        tests.append((f"s{n:03}", "sumn", str(n), f"{n*(n+1)//2}\r\n".encode(), b"Sum: "))
    commands = ["@echo off", "echo PENDING>check.ok"]
    for case, program, value, _, _ in tests:
        redirect = ""
        if value is not None:
            dos_text(WORK / f"{case}.in", value + "\n")
            redirect = f" < {case}.in"
        commands += [f"{program}.exe{redirect} > {case}.out", "if errorlevel 1 goto failed"]
    for _, _, name in PROGRAMS:
        commands.append(f"debug {name}.exe < {name}.dbg > {name}.dis")
    # Direct DEBUG E writes both code and data to memory; no source EXE is loaded.
    dos_text(WORK / "memory.dbg", (ROOT / "homework1" / "memory.dbg").read_text())
    commands += ["debug < memory.dbg > memory.dis", "echo PASS>check.ok", "exit",
                 ":failed", "echo FAIL>check.ok", "exit"]
    dos_text(WORK / "checkall.bat", "\n".join(commands) + "\n")
    dos_session("checkall.bat")
    assert (WORK / "check.ok").read_text().strip() == "PASS"
    for case, program, value, expected, marker in tests:
        actual = (WORK / f"{case}.out").read_bytes()
        if marker:
            actual = actual.split(marker, 1)[1]
        assert actual == expected, (case, program, value, actual, expected)
    memory = (WORK / "memory.dis").read_text(encoding="ascii")
    assert "Hello world!" in memory and "Program terminated normally (0000)" in memory
    shutil.copyfile(WORK / "memory.dis", ROOT / "homework1" / "memory_debug.txt")
    shutil.copyfile(WORK / "link.log", ROOT / "homework1" / "link.txt")
    shutil.copyfile(WORK / "hello.map", ROOT / "homework1" / "hello.map")
    for folder, _, name in PROGRAMS:
        directory = ROOT / folder
        for extension in ("exe", "lst", "dis"):
            shutil.copyfile(WORK / f"{name}.{extension}", directory / f"{name}.{extension}")
        dis = (directory / f"{name}.dis").read_text(encoding="ascii")
        assert "INT" in dis and "21" in dis, name
        case = {"sumn": "s100", "hex2dec": "h255", "dec2hex": "d65535"}.get(name, name)
        shutil.copyfile(WORK / f"{case}.out", directory / f"{name}.out")
    summary = {
        "result": "PASS", "assembly_target": "8086 / 16-bit DOS MZ",
        "c_target": run([GCC, "-dumpmachine"]).stdout.decode().strip(),
        "dos_execution_cases": len(tests), "c_execution_cases": 101,
        "coverage": {"hello": "OMF assembly + separate DOS link + execution + DEBUG disassembly",
                     "debug_memory": "DEBUG E writes code and data, executes Hello world",
                     "ascii": "LOOP, conditional jumps, C; exact 54-byte identical output",
                     "sum_storage": "register, data segment, stack: all print 5050",
                     "sum_input": "all n=1..100 for both DOS assembly and C",
                     "hex_to_decimal": "all 00..FF upper/lowercase, single digits 0..f",
                     "decimal_to_hex": decimals},
    }
    (evidence / "verification.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(tests)} DOS cases + 101 C cases; DEBUG memory and all disassemblies verified.")


if __name__ == "__main__":
    main()
