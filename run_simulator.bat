@echo off
set BASE_PATH=%~dp0\..
cd %BASE_PATH%
set PYTHONPATH=%PYTHONPATH%;%BASE_PATH%
python interactive_leds\src\simulator\simulator.py interactive_leds.src.games.%*
cd %~dp0
