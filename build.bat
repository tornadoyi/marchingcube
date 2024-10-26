@echo off
set CUR_PATH=%~dp0


pyinstaller --add-data "%CUR_PATH%\marchingcube\dataset:dataset" "%CUR_PATH%\marchingcube\main.py"