#!/bin/bash
# 印刷报价系统 - 前端启动脚本

echo "========================================"
echo "  印刷报价系统 - 前端服务启动"
echo "========================================"
echo ""

# 检查依赖
if [ ! -d "node_modules" ]; then
    echo "⚠️  依赖未安装，正在安装..."
    npm install
else
    echo "✅ 依赖已安装"
fi
echo ""

# 启动服务
echo "🚀 启动前端服务..."
echo "前端界面: http://localhost:5173"
echo ""
echo "按 Ctrl+C 停止服务"
echo "========================================"
echo ""

npm run dev
