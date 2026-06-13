# 印刷报价系统

基于参考站 yinshuabaojia.com 功能逻辑的原创印刷在线报价系统。

## 技术栈

- **前端**: Vue 3 + TypeScript + Vite
- **后端**: Python 3.11+ + FastAPI
- **数据库**: MySQL 8.0+
- **UI风格**: 参考 yinshuabaojia.com 的样式风格

## 项目结构

```
print/
├── frontend/          # Vue 3 前端项目
├── backend/           # FastAPI 后端项目
├── database/          # 数据库脚本和种子数据
├── docs/              # 项目文档
└── README.md
```

## 当前进度

- [x] 项目初始化
- [ ] 数据库设计
- [ ] 无碳联单报价计算引擎
- [ ] 前端表单界面
- [ ] API 接口开发

## 快速开始

### 后端启动
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 前端启动
```bash
cd frontend
npm install
npm run dev
```

## 核心功能模块

### 第一期：无碳联单报价
- 前台表单：成品尺寸、订单数量、联数、页数、印刷颜色、纸张克重、后道工序
- 报价计算引擎：纸款计算、印刷费计算、后加工费计算、成本附加
- 输出：阶梯价格表、成本明细、报价单

### 后续扩展
- 更多品类（彩盒、画册、不干胶等）
- 参数配置管理后台
- 用户系统与订单管理
- 印刷商城集成
