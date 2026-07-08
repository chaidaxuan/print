# 印刷报价系统 —— 腾讯云 Windows Server 2022 部署文档

> 目标：把本项目部署到腾讯云 Windows Server 2022，**内部/临时使用，直接跑 dev 服务**。
> 技术栈：前端 Vue3 + Vite（端口 5173），后端 FastAPI + uvicorn（端口 8000），数据库 MySQL 8.0。

---

## 一、需要安装的软件（三样）

| 软件 | 版本要求 | 用途 | 下载 |
|------|----------|------|------|
| Python | **3.11**（不要用 3.12+） | 跑后端 FastAPI | python.org，Windows installer，安装时**务必勾选 Add Python to PATH** |
| Node.js | **20 LTS**（≥18 即可） | 跑前端 Vite | nodejs.org，Windows MSI |
| MySQL | **8.0** Community Server | 数据库 | mysql.com，安装时记住 root 密码 |

---

## 二、部署步骤

### 1. 数据库初始化

安装完 MySQL 后，打开命令行执行（`-p` 后会提示输入 root 密码）：

```bash
mysql -u root -p -e "CREATE DATABASE printing_quote CHARACTER SET utf8mb4;"
mysql -u root -p printing_quote < database/schema.sql
mysql -u root -p printing_quote < database/migration_machine_color_fee.sql
```

> 说明：`database/schema.sql` 是主表结构，`database/migration_machine_color_fee.sql` 是机器颜色费迁移，两个都要导入。

### 2. 后端（FastAPI）

先在 `backend/` 目录下新建一个 `.env` 文件，内容如下（把密码换成实际的 MySQL root 密码）：

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=printing_quote
```

然后安装依赖并启动：

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

> ⚠️ 临时跑**不要加 `--reload`**。加了 reload 会有多进程残留，改代码后可能返回旧结果。

后端依赖已锁定版本（在 `backend/requirements.txt`）：
```
fastapi==0.115.0
uvicorn[standard]==0.32.0
pydantic==2.9.2
pydantic-settings==2.6.0
sqlalchemy==2.0.36
pymysql==1.1.1
python-dotenv==1.0.1
python-multipart==0.0.12
```

### 3. 前端（Vue3 + Vite）

新开一个命令行窗口：

```bash
cd frontend
npm install
npm run dev
```

> 前端已配置 `host: true` 和 `allowedHosts: true`，会绑定所有网卡，可通过服务器 IP 访问。
> 前端通过 `proxy /api → localhost:8000` 转发到后端，**所以浏览器只需访问 5173，不会有跨域(CORS)问题**。

---

## 三、开放端口（关键，两处都要做）

内部临时用 dev 服务时，浏览器**只需要访问 5173**（8000 被 vite 代理，不用对外开放）。

### 1. 腾讯云控制台 → 安全组
- 添加**入站规则**：放行 TCP 端口 **5173**，来源按需（临时可 `0.0.0.0/0`，更安全可限定你的 IP）

### 2. 服务器内 Windows 防火墙
- 高级安全 Windows Defender 防火墙 → 入站规则 → 新建规则 → 端口 → TCP **5173** → 允许连接

---

## 四、访问

浏览器打开：

```
http://服务器公网IP:5173
```

---

## 五、注意事项

1. **dev 服务仅适合内部/临时使用**：没有认证、进程崩了不会自动重启、性能未优化。如需长期对外服务，应改用 `npm run build` 生成静态文件 + 后端注册为 Windows 服务的正式方案。
2. **MySQL 密码安全**：不要用弱密码（如 root/root）暴露在公网。安全组尽量限定来源 IP。
3. **两个命令行窗口**：后端和前端各占一个窗口，都要保持运行。关闭窗口服务就停了。
4. **启动顺序**：先起 MySQL（服务默认自启）→ 再起后端 → 最后起前端。
