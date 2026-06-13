# 印刷报价系统 - 快速启动指南

## 项目概述

这是一个基于 **Vue 3 + TypeScript + Python FastAPI + MySQL** 的印刷在线报价系统。当前已完成「无碳联单」报价功能的核心开发。

## 技术栈

- **前端**: Vue 3.4 + TypeScript + Vite 5.0 + Pinia
- **后端**: Python 3.11+ + FastAPI + SQLAlchemy
- **数据库**: MySQL 8.0+
- **UI 风格**: 参考 yinshuabaojia.com（原创实现）

## 目录结构

```
print/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── models/         # 数据库模型
│   │   ├── schemas/        # Pydantic 模型
│   │   ├── routers/        # API 路由
│   │   ├── services/       # 业务逻辑（报价引擎）
│   │   ├── config.py       # 配置
│   │   └── database.py     # 数据库连接
│   ├── main.py             # FastAPI 入口
│   ├── requirements.txt    # Python 依赖
│   └── .env.example        # 环境变量示例
│
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── components/    # Vue 组件
│   │   │   ├── Layout/    # 布局组件（Header、Nav、Footer）
│   │   │   └── Quote/     # 报价组件（表单、结果）
│   │   ├── views/         # 页面视图
│   │   ├── api/           # API 请求
│   │   ├── types/         # TypeScript 类型定义
│   │   ├── styles/        # 全局样式（设计系统变量）
│   │   ├── App.vue        # 根组件
│   │   └── main.ts        # 入口文件
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── database/               # 数据库脚本
│   └── schema.sql         # 完整建表 SQL（含初始数据）
│
├── docs/                   # 文档
│   └── UI_IMPLEMENTATION_PLAN.md  # UI 复刻实施计划
│
└── README.md              # 项目说明
```

---

## 一、环境准备

### 1. 安装依赖

#### 系统要求
- **Node.js**: 18+ 
- **Python**: 3.11+
- **MySQL**: 8.0+

#### 检查版本
```bash
node -v      # 应显示 v18 或更高
python -V    # 应显示 3.11 或更高
mysql --version
```

---

## 二、数据库初始化

### 1. 创建数据库
```bash
mysql -u root -p
```

```sql
CREATE DATABASE printing_quote CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

### 2. 导入表结构和初始数据
```bash
mysql -u root -p printing_quote < database/schema.sql
```

### 3. 验证导入
```bash
mysql -u root -p printing_quote
```

```sql
SHOW TABLES;
SELECT * FROM product_categories;
SELECT * FROM product_sizes;
```

你应该看到：
- `product_categories` 表中有「无碳联单」记录
- `product_sizes` 表中有 5 条尺寸记录
- `printing_machines` 表中有 4 台机器
- `paper_specs` 表中有 3 种纸张规格

---

## 三、后端启动

### 1. 进入后端目录
```bash
cd backend
```

### 2. 创建虚拟环境（推荐）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 配置环境变量
复制 `.env.example` 并重命名为 `.env`，修改数据库配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=你的MySQL密码
DB_NAME=printing_quote

APP_NAME=印刷报价系统
DEBUG=True
```

### 5. 启动后端服务
```bash
# 开发模式（自动重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 或直接运行
python main.py
```

### 6. 验证后端
访问以下地址：
- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/health
- **获取尺寸列表**: http://localhost:8000/api/quote/sizes
- **获取印刷颜色**: http://localhost:8000/api/quote/colors

---

## 四、前端启动

### 1. 打开新终端，进入前端目录
```bash
cd frontend
```

### 2. 安装依赖
```bash
npm install
```

如果速度慢，可以使用国内镜像：
```bash
npm install --registry=https://registry.npmmirror.com
```

### 3. 启动前端开发服务器
```bash
npm run dev
```

### 4. 访问前端
浏览器打开：**http://localhost:5173**

---

## 五、功能测试

### 1. 无碳联单报价测试

**测试步骤：**
1. 访问 http://localhost:5173
2. 左侧表单默认值：
   - 成品尺寸: 32开(210×140)A5
   - 订单数量: 100本
   - 联数: 三联
   - 每本页数: 99页
   - 印刷颜色: 单黑
   - 纸张克重: 50克
   - 后道工序: 装订(胶左) ✓
3. 点击「自助报价」按钮
4. 右侧应显示：
   - 阶梯价格表（100/200/300/400/500 本）
   - 成本明细（可点击「成本明细」查看）
   - 报价摘要

**预期结果：**
- 100本总价约 **634元**，单价 **6.34元/本**
- 成本结构：
  - 纸款: ~254元
  - 印刷费: ~120元
  - 后加工费: ~20元
  - 生产成本: ~394元
  - 成本附加: ~240元
  - 总成本: ~634元

### 2. API 测试

使用 Postman 或 curl 测试：

```bash
# 计算报价
curl -X POST "http://localhost:8000/api/quote/liandan" \
  -H "Content-Type: application/json" \
  -d '{
    "size_id": 1,
    "quantity": 100,
    "sheet_count": 3,
    "pages_per_book": 99,
    "color_code": "single_black",
    "gram_weight": 50,
    "post_processing": ["binding_left"]
  }'
```

---

## 六、常见问题

### 1. 后端启动失败

**问题**: `ModuleNotFoundError: No module named 'fastapi'`
**解决**: 确认已激活虚拟环境并安装依赖
```bash
pip install -r requirements.txt
```

**问题**: 数据库连接失败
**解决**: 检查 `.env` 文件中的数据库配置是否正确

### 2. 前端启动失败

**问题**: `Cannot find module '@/xxx'`
**解决**: 确认已安装依赖
```bash
npm install
```

**问题**: API 请求 CORS 错误
**解决**: 确认后端已启动，并检查 `backend/app/config.py` 中的 `CORS_ORIGINS` 配置

### 3. 计算结果不正确

**问题**: 价格计算结果与预期不符
**解决**: 
- 检查 `system_params` 表中的参数（成本附加率、损耗率）
- 检查 `paper_specs` 表中的纸张价格
- 检查 `printing_machines` 表中的机器参数

---

## 七、开发指南

### 1. 修改成本附加率
```sql
UPDATE system_params 
SET param_value = '0.5'   -- 修改为 50%
WHERE param_key = 'cost_markup_rate';
```

### 2. 添加新的成品尺寸
```sql
INSERT INTO product_sizes (category_id, name, width, height, code, sort_order)
VALUES (1, '自定义尺寸', 200, 150, 'custom', 10);
```

### 3. 修改纸张价格
```sql
UPDATE paper_specs 
SET price_per_sheet = 1.00
WHERE gram_weight = 50;
```

### 4. 前端样式调整
所有设计系统变量定义在 `frontend/src/styles/index.css` 中：
```css
:root {
  --primary-color: #3498db;    /* 主色 */
  --spacing-md: 16px;          /* 间距 */
  --border-radius-md: 4px;     /* 圆角 */
  /* ... */
}
```

### 5. 添加新的报价品类
1. 在 `product_categories` 表中添加品类
2. 在 `backend/app/services/` 创建对应的计算引擎
3. 在 `backend/app/routers/quote.py` 添加 API 路由
4. 在前端创建对应的表单组件

---

## 八、下一步计划

### Phase 2: 表单优化（当前进度：80%）
- [x] 7个核心表单字段组件
- [ ] 表单实时验证
- [ ] 自定义尺寸输入框
- [ ] 后道工序动态配置

### Phase 3: 结果展示优化
- [ ] 多币种汇率实时转换
- [ ] 客户类型价格差异化
- [ ] 报价单 PDF 导出
- [ ] 打印功能

### Phase 4: 更多品类
- [ ] 彩盒彩箱报价
- [ ] 专版不干胶报价
- [ ] 画册报价
- [ ] 纸袋报价

### Phase 5: 管理后台
- [ ] 参数配置界面
- [ ] 用户管理
- [ ] 订单管理
- [ ] 数据报表

---

## 九、部署上线

### 生产环境配置

**后端部署（使用 Gunicorn）：**
```bash
pip install gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**前端构建：**
```bash
cd frontend
npm run build
```
构建产物在 `frontend/dist/` 目录，使用 Nginx 部署。

**Nginx 配置示例：**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # 前端静态文件
    location / {
        root /var/www/printing-quote/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 十、技术支持

- **项目文档**: `docs/UI_IMPLEMENTATION_PLAN.md`
- **API 文档**: http://localhost:8000/docs（后端启动后）
- **参考站点**: yinshuabaojia.com（仅功能参考，不复制源码）

---

## 附录：核心文件清单

### 后端核心文件
- `backend/main.py` - FastAPI 应用入口
- `backend/app/services/quote_engine.py` - 报价计算引擎核心逻辑
- `backend/app/routers/quote.py` - 报价 API 路由
- `backend/app/models/` - 数据库模型定义

### 前端核心文件
- `frontend/src/App.vue` - 根组件
- `frontend/src/views/LiandanQuote.vue` - 无碳联单报价页面
- `frontend/src/components/Quote/QuoteForm.vue` - 报价表单组件
- `frontend/src/components/Quote/QuoteResult.vue` - 报价结果组件
- `frontend/src/styles/index.css` - 设计系统变量

### 配置文件
- `backend/.env` - 后端环境变量（需自行创建）
- `frontend/vite.config.ts` - Vite 配置（API 代理）
- `database/schema.sql` - 数据库初始化脚本

---

**祝开发顺利！** 🎉
