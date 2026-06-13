@echo off
REM 印刷报价系统 - 后端启动脚本 (Windows)

echo ========================================
echo   印刷报价系统 - 后端服务启动
echo ========================================
echo.

REM 检查 .env 文件
if not exist .env (
    echo ❌ 错误: .env 文件不存在
    echo 请先复制 .env.example 为 .env 并配置数据库密码
    pause
    exit /b 1
)

echo ✅ 环境变量文件已找到
echo.

REM 启动服务
echo 🚀 启动后端服务...
echo API 文档: http://localhost:8000/docs
echo 健康检查: http://localhost:8000/health
echo.
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
