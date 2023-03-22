@echo off
if not exist "venv" (
    echo Creating a new virtual environment...
    python -m venv venv
)

echo Activating the virtual environment...
call venv\Scripts\activate

echo Launching the PB&J Convertenator! er well the Python to Java Converter...
python Python-to-Java.py

pause