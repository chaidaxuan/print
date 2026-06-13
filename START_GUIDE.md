# 🚀 印刷报价系统 - 快速启动指令

## 当前准备状态 ✅

- ✅ Python 3.11.9 已安装
- ✅ Node.js 22.14.0 已安装  
- ✅ 后端依赖已安装（FastAPI、SQLAlchemy 等）
- ✅ 前端依赖已安装（Vue 3、Vite 等，共 78 个包）
- ✅ `.env` 配置文件已存在
- ✅ 启动脚本已创建

---

## 启动前的最后一步：初始化数据库

### 方法 1: 使用 MySQL 命令行（推荐）
```bash
# 进入 MySQL
mysql -u root -p

# 创建数据库
CREATE DATABASE printing_quote CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

# 导入表结构和数据
mysql -u root -p printing_quote < database/schema.sql

# 验证导入
mysql -u root -p printing_quote -e "SHOW TABLES; SELECT * FROM product_categories;"
```

### 方法 2: 使用 MySQL Workbench（图形化）
1. 打开 MySQL Workbench
2. 连接到本地数据库
3. 执行 SQL: `CREATE DATABASE printing_quote CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
4. 选择 `printing_quote` 数据库
5. 菜单: File → Run SQL Script → 选择 `database/schema.sql` → 运行

### 方法 3: 如果 MySQL 未安装
请先安装 MySQL:
- Windows: https://dev.mysql.com/downloads/installer/
- 或使用 XAMPP/WAMP（内含 MySQL）

---

## 启动服务（3种方法）

### 方法 1: 使用启动脚本（最简单）⭐

#### Windows 用户:
```bash
# 终端 1: 启动后端
cd backend
start.bat

# 终端 2: 启动前端
cd frontend  
start.bat
```

#### Linux/Mac 用户:
```bash
# 终端 1: 启动后端
cd backend
chmod +x start.sh
./start.sh

# 终端 2: 启动前端
cd frontend
chmod +x start.sh
./start.sh
```

### 方法 2: 手动启动

#### 后端（终端 1）:
```bash
cd backend
uvicorn main:app --reload
```

#### 前端（终端 2）:
```bash
cd frontend
npm run dev
```

### 方法 3: VS Code 集成终端
1. 在 VS Code 中打开项目
2. 打开两个终端（Terminal → Split Terminal）
3. 终端 1 执行后端启动命令
4. 终端 2 执行前端启动命令

---

## 访问地址

启动成功后：

### 🌐 前端界面
**http://localhost:5173**

### 📚 API 文档（Swagger UI）
**http://localhost:8000/docs**

### 🏥 健康检查
**http://localhost:8000/health**

---

## 快速测试

1. 访问 http://localhost:5173
2. 左侧表单使用默认值（已填好）
3. 点击「自助报价」按钮
4. 右侧应显示：
   - 单价: 6.34元/本
   - 总价: 634.00元
   - 阶梯价格表（5行）
5. 点击「成本明细」查看详细计算

---

## 常见问题

### ❌ 后端启动失败: 数据库连接错误
**解决**: 
1. 确认 MySQL 已启动
2. 检查 `backend/.env` 中的密码是否正确
3. 确认数据库 `printing_quote` 已创建

### ❌ 前端启动失败: 端口 5173 被占用
**解决**:
```bash
# 查看占用进程
netstat -ano | findstr 5173

# 结束进程（Windows）
taskkill /F /PID <进程号>

# 或修改端口
# 编辑 frontend/vite.config.ts
server: { port: 5174 }
```

### ❌ API 调用失败: CORS 错误
**解决**:
1. 确认后端已启动
2. 检查 `backend/app/config.py` 中的 `CORS_ORIGINS` 配置

---

## 停止服务

在运行服务的终端中按 `Ctrl + C` 停止

---

## 下一步

启动成功后，您可以：
1. 📖 阅读 [PROJECT_STATUS.md](PROJECT_STATUS.md) 了解待办任务
2. 🔧 修改代码并实时查看效果（热重载）
3. 🧪 测试不同的报价参数
4. 💡 开始添加新功能

---

## 文件位置

- 后端启动脚本: `backend/start.bat` (Windows) 或 `backend/start.sh` (Linux/Mac)
- 前端启动脚本: `frontend/start.bat` (Windows) 或 `frontend/start.sh` (Linux/Mac)
- 环境配置: `backend/.env`
- 数据库脚本: `database/schema.sql`

---

**准备完成！现在可以启动项目了。** 🎉

有任何问题请查看 [QUICKSTART.md](QUICKSTART.md) 的完整说明。
