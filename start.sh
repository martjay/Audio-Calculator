#!/bin/bash

# 设置颜色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查Python3是否安装
echo -e "${GREEN}检查Python环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误：未安装Python3！${NC}"
    echo "请先安装Python3"
    exit 1
fi

# 检查icon.ico是否存在
if [ ! -f "icon.ico" ]; then
    echo -e "${YELLOW}警告：未找到icon.ico文件！${NC}"
fi

# 检查并创建虚拟环境
if [ ! -d "venv" ]; then
    echo -e "${GREEN}首次运行，创建虚拟环境...${NC}"
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 检查requirements.txt是否有更新
if [ -f "requirements.txt.old" ]; then
    if ! cmp -s "requirements.txt" "requirements.txt.old"; then
        echo -e "${GREEN}检测到依赖更新，正在安装新依赖...${NC}"
        pip install -r requirements.txt
        cp requirements.txt requirements.txt.old
    fi
else
    echo -e "${GREEN}首次安装依赖...${NC}"
    pip install -r requirements.txt
    cp requirements.txt requirements.txt.old
fi

# 启动程序
echo -e "${GREEN}启动程序...${NC}"
python3 audio_calculator.py

# 退出虚拟环境
deactivate 