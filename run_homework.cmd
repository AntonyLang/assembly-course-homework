@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
python "%~dp0scripts\build_all.py"
if errorlevel 1 goto done
echo C version - ASCII:
"%~dp0homework2\ascii_c.exe"
python "%~dp0scripts\open_dos.py" --demo
:done
pause
