"""Open the existing DOS work directory after the unified build."""
import argparse
import subprocess
from build_all import DOSBOX, ROOT, WORK

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--demo", action="store_true")
args = parser.parse_args()
commands = ["cls"]
if args.demo:
    commands += ["echo Homework 1 - Hello:", "hello", "echo.",
                 "echo Homework 2 - LOOP and conditional jumps:", "loop", "jump", "echo.",
                 "echo Homework 3 - register, data segment, stack:",
                 "sumreg", "sumdata", "sumstack", "echo."]
commands += ["echo Commands: HELLO, LOOP, JUMP, SUMREG, SUMDATA, SUMSTACK",
             "echo Input programs: SUMN, HEX2DEC, DEC2HEX",
             "echo Debug: DEBUG HELLO.EXE or DEBUG LOOP.EXE",
             "echo Direct memory experiment: see homework1/README.md",
             "echo Exit: EXIT"]
arguments = [str(DOSBOX), "-conf", str(ROOT / "homework2" / "dosbox-x.conf"),
             "-nopromptfolder", "-fastlaunch"]
for command in commands:
    arguments += ["-c", command]
subprocess.run(arguments, cwd=WORK, check=True)
