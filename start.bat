@echo off
chcp 65001 > nul

echo 检查Python环境...
python --version 2>NUL
if errorlevel 1 (
    echo 错误：未安装Python！
    echo Error: Python is not installed!
    pause
    exit /b 1
)

echo 检查Visual C++ Redistributable...
reg query "HKLM\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64" /v Version >nul 2>&1
if errorlevel 1 (
    echo 警告：未检测到Visual C++ Redistributable 2015-2022！
    echo 请先安装Visual C++ Redistributable 2015-2022 x64版本
    echo 下载地址：https://aka.ms/vs/17/release/vc_redist.x64.exe
    start https://aka.ms/vs/17/release/vc_redist.x64.exe
    pause
    exit /b 1
)

if not exist "venv" (
    echo 首次运行，创建虚拟环境...
    python -m venv venv
)

call venv\Scripts\activate

:: 检查requirements.txt是否有更新
if exist "requirements.txt.old" (
    fc /b requirements.txt requirements.txt.old >nul
    if errorlevel 1 (
        echo 检测到依赖更新，正在安装新依赖...
        pip install -r requirements.txt
        copy /y requirements.txt requirements.txt.old
    )
) else (
    echo 首次安装依赖...
    pip install -r requirements.txt
    copy requirements.txt requirements.txt.old
)

echo 启动程序...
python audio_calculator.py
call venv\Scripts\deactivate
pause 