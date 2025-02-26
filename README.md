# Audio Calculator | 音频计算器

[English](#english) | [中文](#chinese)

## English

### Introduction
Audio Calculator is a professional tool designed for music producers and audio engineers. It helps calculate reverb and delay parameters based on the song's BPM (Beats Per Minute).

### Features
- BPM-based reverb parameter calculation
- BPM-based delay parameter calculation
- Manual BPM detection through tapping
- Support for both light and dark themes
- Multi-language support (English/Chinese)
- Always-on-top window option
- Direct link to Audiobar

### Installation & Running

#### Windows Users
1. Download the latest release
2. Double-click `start.bat` to run the application directly
3. Or run the standalone `AudioCalculator.exe` if you downloaded the release version

Build from source:
1. Clone this repository
2. Run `build_exe.bat` to create the executable
3. Find the executable in the `dist` folder

#### macOS Users
1. Download the latest release
2. Open Terminal in the application folder
3. Make the start script executable: `chmod +x start.sh`
4. Run `./start.sh` to start the application

Build from source:
1. Clone this repository
2. Make scripts executable: `chmod +x start.sh build_app.sh`
3. Run `./build_app.sh` to create the application
4. Find the app in the `dist` folder

### Dependencies
- Python 3.8+
- PyQt6
- pyperclip
- pyinstaller (for building)

## Chinese

### 简介
音频计算器是一款专为音乐制作人和音频工程师设计的专业工具。它可以根据歌曲的 BPM（每分钟节拍数）计算混响和延迟参数。

### 功能特点
- 基于 BPM 的混响参数计算
- 基于 BPM 的延迟参数计算
- 通过点击或使用快捷键手动检测 BPM
- 支持浅色和深色主题
- 多语言支持（中文/英文）
- 窗口置顶选项

### 安装和运行

#### Windows 用户
1. 下载最新版本
2. 双击 `start.bat` 直接运行应用程序
3. 或者运行独立的 `AudioCalculator.exe`（如果您下载了发布版本）

从源码构建：
1. 克隆此仓库
2. 运行 `build_exe.bat` 创建可执行文件
3. 在 `dist` 文件夹中找到可执行文件

#### macOS 用户
1. 下载最新版本
2. 在终端中进入应用程序文件夹
3. 使启动脚本可执行：`chmod +x start.sh`
4. 运行 `./start.sh` 启动应用程序

从源码构建：
1. 克隆此仓库
2. 使脚本可执行：`chmod +x start.sh build_app.sh`
3. 运行 `./build_app.sh` 创建应用程序
4. 在 `dist` 文件夹中找到应用程序

### 依赖项
- Python 3.8+
- PyQt6
- pyperclip
- pyinstaller (用于构建)

### 使用说明
1. 输入BPM：直接在输入框中输入数值
2. 测量BPM：点击"手动测速"，然后通过点击按钮或按空格键来计算
3. 查看参数：程序会自动计算并显示所有混响和延迟参数

--- 