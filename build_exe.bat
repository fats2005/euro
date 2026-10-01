@echo off
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name EuroRoadRacer main.py
echo EXE created at dist\EuroRoadRacer.exe
pause
