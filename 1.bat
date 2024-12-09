@echo off
echo Project Structure: > debug_info.txt
dir /s /b >> debug_info.txt
echo. >> debug_info.txt
echo File Contents: >> debug_info.txt

for %%f in (*.py) do (
    echo ### %%f ### >> debug_info.txt
    type %%f >> debug_info.txt
    echo. >> debug_info.txt
)