# 印刷报价系统 - 项目文件树

```
print/
│
├── 📄 README.md                          # 项目说明
├── 📄 QUICKSTART.md                      # ⭐ 快速启动指南（必读）
├── 📄 PROJECT_STATUS.md                  # ⭐ 项目状态报告（跨会话必读）
│
├── 📁 backend/                           # Python FastAPI 后端
│   ├── 📄 main.py                        # ⭐ 应用入口
│   ├── 📄 requirements.txt               # Python 依赖列表
│   ├── 📄 .env.example                   # 环境变量模板（需复制为 .env）
│   │
│   └── 📁 app/
│       ├── 📄 config.py                  # ⭐ 配置文件（数据库连接等）
│       ├── 📄 database.py                # ⭐ 数据库连接管理
│       │
│       ├── 📁 models/                    # SQLAlchemy 数据模型（8个表）
│       │   ├── 📄 __init__.py
│       │   ├── 📄 category.py            # 产品品类表
│       │   ├── 📄 size.py                # 成品尺寸表
│       │   ├── 📄 machine.py             # 印刷机器参数表
│       │   ├── 📄 paper.py               # 纸张规格与价格表
│       │   ├── 📄 color.py               # 印刷颜色配置表
│       │   ├── 📄 processing.py          # 后道工序价格表
│       │   ├── 📄 param.py               # 系统参数配置表
│       │   └── 📄 quote.py               # 报价记录表
│       │
│       ├── 📁 schemas/                   # Pydantic 请求/响应模型
│       │   ├── 📄 __init__.py
│       │   └── 📄 quote.py               # ⭐ 报价相关的数据模型
│       │
│       ├── 📁 services/                  # 业务逻辑层
│       │   └── 📄 quote_engine.py        # ⭐⭐⭐ 核心报价计算引擎
│       │                                 #     (纸款/印刷费/后工/成本附加)
│       │
│       └── 📁 routers/                   # API 路由
│           ├── 📄 __init__.py
│           └── 📄 quote.py               # ⭐ 报价相关 API 端点
│                                         #     GET /sizes, /colors, /post-processing
│                                         #     POST /liandan
│
├── 📁 frontend/                          # Vue 3 + TypeScript 前端
│   ├── 📄 index.html                     # HTML 入口
│   ├── 📄 package.json                   # npm 依赖配置
│   ├── 📄 vite.config.ts                 # ⭐ Vite 配置（含 API 代理）
│   ├── 📄 tsconfig.json                  # TypeScript 配置
│   ├── 📄 tsconfig.node.json             # TypeScript Node 配置
│   │
│   └── 📁 src/
│       ├── 📄 main.ts                    # ⭐ 应用入口
│       ├── 📄 App.vue                    # ⭐ 根组件
│       │
│       ├── 📁 styles/
│       │   └── 📄 index.css              # ⭐⭐ 设计系统变量定义
│       │                                 #     (颜色/字体/间距/圆角/阴影)
│       │
│       ├── 📁 types/
│       │   └── 📄 quote.ts               # ⭐ TypeScript 类型定义
│       │
│       ├── 📁 api/
│       │   └── 📄 quote.ts               # ⭐ API 请求封装
│       │
│       ├── 📁 utils/
│       │   └── 📄 request.ts             # Axios 拦截器配置
│       │
│       ├── 📁 components/
│       │   ├── 📁 Layout/                # 布局组件
│       │   │   ├── 📄 Header.vue         # 顶部导航（系统标题 + 用户信息）
│       │   │   ├── 📄 MainNav.vue        # 主导航菜单（首页/报价/彩盒等）
│       │   │   ├── 📄 Breadcrumb.vue     # 面包屑导航
│       │   │   └── 📄 Footer.vue         # 底部信息
│       │   │
│       │   └── 📁 Quote/                 # 报价核心组件
│       │       ├── 📄 QuoteForm.vue      # ⭐⭐⭐ 报价表单组件
│       │       │                         #     (尺寸/数量/联数/页数/颜色/克重/工序)
│       │       └── 📄 QuoteResult.vue    # ⭐⭐⭐ 报价结果展示组件
│       │                                 #     (价格表/成本明细/企业信息)
│       │
│       └── 📁 views/
│           └── 📄 LiandanQuote.vue       # ⭐ 无碳联单报价页面（主页面）
│
├── 📁 database/                          # 数据库脚本
│   └── 📄 schema.sql                     # ⭐⭐ 完整建表 SQL + 初始数据
│                                         #     (8张表 + 演示数据)
│
├── 📁 docs/                              # 项目文档
│   └── 📄 UI_IMPLEMENTATION_PLAN.md      # ⭐⭐ UI 复刻实施计划
│                                         #     (完整的设计规范/配色/尺寸/组件拆分)
│
└── 📁 参考资料/
    ├── 📄 liandan-form-screenshot.png    # 参考站点截图
    ├── 📄 liandan-form-structure.md      # 页面结构快照（YAML）
    └── 📄 home-full.png                  # 首页截图
```

---

## 文件说明

### 🔴 核心文件（必须理解）

| 文件 | 作用 | 重要性 |
|-----|------|--------|
| `backend/app/services/quote_engine.py` | 报价计算引擎核心逻辑 | ⭐⭐⭐ |
| `frontend/src/components/Quote/QuoteForm.vue` | 报价表单组件 | ⭐⭐⭐ |
| `frontend/src/components/Quote/QuoteResult.vue` | 报价结果展示 | ⭐⭐⭐ |
| `database/schema.sql` | 数据库结构定义 | ⭐⭐⭐ |

### 🟡 重要文件（需要熟悉）

| 文件 | 作用 | 重要性 |
|-----|------|--------|
| `backend/app/routers/quote.py` | API 路由定义 | ⭐⭐ |
| `backend/app/models/*.py` | 数据库模型（8个表） | ⭐⭐ |
| `frontend/src/App.vue` | 前端根组件 | ⭐⭐ |
| `frontend/src/styles/index.css` | 设计系统变量 | ⭐⭐ |
| `docs/UI_IMPLEMENTATION_PLAN.md` | UI 实施计划 | ⭐⭐ |

### 🟢 配置文件（按需修改）

| 文件 | 作用 | 重要性 |
|-----|------|--------|
| `backend/.env` | 环境变量（数据库密码等）| ⭐ |
| `backend/app/config.py` | 后端配置 | ⭐ |
| `frontend/vite.config.ts` | Vite 配置（API 代理）| ⭐ |
| `backend/requirements.txt` | Python 依赖 | ⭐ |
| `frontend/package.json` | npm 依赖 | ⭐ |

### 🔵 文档（跨会话必读）

| 文件 | 作用 | 重要性 |
|-----|------|--------|
| `QUICKSTART.md` | 快速启动指南 | ⭐⭐⭐ |
| `PROJECT_STATUS.md` | 项目状态报告 | ⭐⭐⭐ |
| `README.md` | 项目说明 | ⭐⭐ |

---

## 文件统计

### 后端（Python + FastAPI）
- **代码文件**: 15 个
- **总行数**: 约 1200 行
- **核心文件**: `quote_engine.py`（约 200 行）

### 前端（Vue 3 + TypeScript）
- **代码文件**: 15 个
- **总行数**: 约 1800 行
- **核心组件**: `QuoteForm.vue`（约 350 行）+ `QuoteResult.vue`（约 400 行）

### 数据库
- **表数量**: 8 张
- **初始数据**: 约 30 条记录

### 文档
- **文档数量**: 4 个
- **总字数**: 约 15000 字

---

## 快速定位指南

### 🔍 想要修改报价计算逻辑？
→ `backend/app/services/quote_engine.py`

### 🔍 想要调整表单字段？
→ `frontend/src/components/Quote/QuoteForm.vue`

### 🔍 想要修改价格表样式？
→ `frontend/src/components/Quote/QuoteResult.vue`

### 🔍 想要添加新的尺寸规格？
→ `database/schema.sql` 的 `product_sizes` 表

### 🔍 想要调整颜色/字体/间距？
→ `frontend/src/styles/index.css` 的 `:root` 变量

### 🔍 想要修改数据库连接？
→ `backend/.env` 文件

### 🔍 想要了解 API 接口？
→ 启动后端后访问 http://localhost:8000/docs

### 🔍 想要了解项目进度？
→ `PROJECT_STATUS.md`

### 🔍 想要快速上手？
→ `QUICKSTART.md`

### 🔍 想要了解 UI 设计规范？
→ `docs/UI_IMPLEMENTATION_PLAN.md`

---

## 开发工作流

### 新增一个报价品类（如彩盒）

```
1. 数据库层
   ├─ database/schema.sql          # 添加品类记录
   └─ backend/app/models/          # 如需新字段，添加模型

2. 后端层
   ├─ backend/app/services/        # 创建 caihe_quote_engine.py
   ├─ backend/app/schemas/quote.py # 添加 CaiheQuoteRequest/Response
   └─ backend/app/routers/quote.py # 添加 POST /caihe 路由

3. 前端层
   ├─ frontend/src/components/Quote/  # 创建 CaiheForm.vue
   ├─ frontend/src/views/             # 创建 CaiheQuote.vue
   └─ frontend/src/api/quote.ts       # 添加 calculateCaiheQuote()
```

### 优化现有功能

```
1. 后端优化
   └─ backend/app/services/quote_engine.py  # 修改计算逻辑

2. 前端优化
   ├─ frontend/src/components/Quote/QuoteForm.vue    # 优化表单交互
   └─ frontend/src/components/Quote/QuoteResult.vue  # 优化结果展示

3. 样式优化
   └─ frontend/src/styles/index.css  # 调整全局变量
```

---

## 项目启动顺序

```bash
# 终端 1: 启动数据库（如未启动）
mysql.server start

# 终端 2: 启动后端
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload

# 终端 3: 启动前端
cd frontend
npm run dev

# 浏览器
打开 http://localhost:5173
```

---

## 代码规范

### 后端（Python）
- 遵循 PEP 8
- 函数名使用 `snake_case`
- 类名使用 `PascalCase`
- 注释使用中文

### 前端（Vue + TypeScript）
- 组件名使用 `PascalCase`
- 函数名使用 `camelCase`
- CSS 类名使用 `kebab-case`
- 注释使用中文
- 使用 Composition API（不用 Options API）

### 数据库（MySQL）
- 表名使用 `snake_case`
- 字段名使用 `snake_case`
- 主键统一命名为 `id`
- 时间戳字段: `created_at`, `updated_at`

---

**最后更新**: 2026-06-14
