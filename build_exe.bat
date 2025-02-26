@echo off
chcp 65001 > nul

if not exist "venv" (
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

:: 先用英文名称打包
venv\Scripts\pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --add-data "icon.ico;." ^
    --name="AudioCalculator" ^
    --version-file=version.txt ^
    audio_calculator.py

:: 删除spec文件
del /f /q "AudioCalculator.spec"

:: 重命名可执行文件
if exist "dist\AudioCalculator.exe" (
    move "dist\AudioCalculator.exe" "dist\音频计算器2025.exe"
)

echo Build completed!
pause 