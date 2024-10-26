@echo off
set "CUR_PATH=%~dp0"


if exist "%CUR_PATH%\marchingcube.egg-info" (
  rmdir /s /q "%CUR_PATH%\marchingcube.egg-info"
)

if exist "%CUR_PATH%\build" (
  rmdir /s /q "%CUR_PATH%\build"
)

if exist "%CUR_PATH%\dist" (
  rmdir /s /q "%CUR_PATH%\dist"
)

if exist "%CUR_PATH%\marchingcube.spec" (
  del "%CUR_PATH%\marchingcube.spec"
)