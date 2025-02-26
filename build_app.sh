#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create and activate virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Build the app using PyInstaller
venv/bin/pyinstaller --noconfirm \
                     --onefile \
                     --windowed \
                     --icon=icon.ico \
                     --add-data "icon.ico:." \
                     --name="AudioCalculator" \
                     --target-arch universal2 \
                     --osx-bundle-identifier "com.audiocalculator.app" \
                     audio_calculator.py

# 如果是macOS系统，创建icns图标
if [ "$(uname)" == "Darwin" ]; then
    # 创建临时图标目录
    mkdir -p icon.iconset
    # 转换ico为png
    sips -s format png icon.ico --out icon.iconset/icon_512x512.png
    # 生成icns文件
    iconutil -c icns icon.iconset
    # 清理临时文件
    rm -rf icon.iconset
    # 将icns文件复制到应用程序包中
    if [ -f "icon.icns" ]; then
        cp icon.icns "dist/AudioCalculator.app/Contents/Resources/"
    fi
fi

echo "Build completed!" 