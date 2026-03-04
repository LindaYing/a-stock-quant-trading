#!/bin/bash

# A股量化交易系统 - 启动脚本

echo "=================================="
echo "🚀 启动 A股量化交易系统"
echo "=================================="

# 检查依赖
echo ""
echo "检查依赖..."

if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit 未安装"
    echo "正在安装..."
    pip3 install streamlit plotly
fi

if ! python3 -c "import plotly" 2>/dev/null; then
    echo "❌ Plotly 未安装"
    echo "正在安装..."
    pip3 install plotly
fi

echo "✅ 依赖检查完成"

# 启动应用
echo ""
echo "=================================="
echo "🌐 启动 Web 界面..."
echo "=================================="
echo ""
echo "📱 访问地址:"
echo "   本地: http://localhost:8501"
echo "   网络: http://$(ipconfig getifaddr en0):8501"
echo ""
echo "💡 提示:"
echo "   - 按 Ctrl+C 停止服务"
echo "   - 手机访问请使用网络地址"
echo ""
echo "=================================="
echo ""

cd "$(dirname "$0")"
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
