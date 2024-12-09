@REM @echo off
@REM echo Project Structure: > debug_info.txt
@REM dir /s /b >> debug_info.txt
@REM echo. >> debug_info.txt
@REM echo File Contents: >> debug_info.txt

@REM for %%f in (*.py) do (
@REM     echo ### %%f ### >> debug_info.txt
@REM     type %%f >> debug_info.txt
@REM     echo. >> debug_info.txt
@REM )

@echo off
if exist debug_info.txt del debug_info.txt

echo Project Structure: > debug_info.txt
dir /s /b >> debug_info.txt
echo. >> debug_info.txt
echo File Contents: >> debug_info.txt

for %%f in (*.py screens\*.py) do (
    echo ### %%f ### >> debug_info.txt
    type "%%f" >> debug_info.txt
    echo. >> debug_info.txt
)