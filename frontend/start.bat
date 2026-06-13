@echo off
REM 印刷报价系统 - 前端启动脚本 (Windows)

echo ========================================
echo   印刷报价系统 - 前端服务启动
echo ========================================
echo.

REM 检查依赖
if not exist node_modules (
    echo ⚠️  依赖未安装，正在安装...
    call npm install
) else (
    echo ✅ 依赖已安装
)
echo.

REM 启动服务
echo 🚀 启动前端服务...
echo 前端界面: http://localhost:5173
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

call npm run dev
