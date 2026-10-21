@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
python "%~dp0scripts\build_all.py"
if errorlevel 1 goto failed
python "%~dp0scripts\open_dos.py"
exit /b
:failed
if errorlevel 1 pause
