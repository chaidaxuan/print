# 无碳联单报价系统 — 开发计划与进度（跨会话可读）

> 本文件是项目的"主计划 + 进度看板"。每次会话开始先读它，结束前更新它。
> 目标：复刻 yinshuabaojia.com 的**无碳联单**全部功能，前端视觉高度一致。

## 版权边界（不可越过）
- ✅ 可做：布局结构、配色、间距、组件排布、交互方式、报价业务逻辑——这些是功能性设计，做到高度一致。
- ❌ 不做：原样下载复用对方的 logo 文件、专有图片素材、品牌文案原文（商标/版权保护）。用原创/通用替代资源还原同样观感。

## 技术栈（已定）
- 前端：Vue 3 + TypeScript + Vite + Pinia + vue-router
- 后端：Python + FastAPI + SQLAlchemy + PyMySQL
- 数据库：MySQL 8.0（库名 printing_quote，root/root，本地 3306）

## 参考站「无碳联单」业务要点（来自记忆 liandan-quote-logic）
- 表单字段：成品尺寸(下拉+自定义)、订单数量(本)、联数(2-6联+每联详情)、每本页数(自动算份数=页数/联数)、
  印刷颜色(正面下拉+背面独立+大实地/高品质勾选)、纸张克重(50/80/108)、后道工序(我要设计/装订胶左胶头/印张交货/加卡纸/打号码/压痕压点线/加封面/印封面/换边联字/打包)、客户、产品名、自填利润率。
- 输出：阶梯数量单价表(100/200/300/400/500本)、多币种(13种)、多客户类型价(6种)、成本明细/报价单/合同单/生产流程单。
- 成本链：纸款+印刷费+后加工=生产成本；生产成本×(1+成本附加率)=总成本；单价=总成本/数量。
- 标准校验案例：32开210×140, 100本, 99页/本三联, 单黑单面, 50克, 装订-胶左 → 参考站示例总价约￥634, 单价6.34。
  （注：演示参数与本系统参数不同，数值不要求完全等于634，但量级与结构需合理。）

## 任务清单与状态
- [x] T1 修复报价引擎无限递归（calculate↔_calculate_ladder_prices）— 已抽出 _calculate_single
- [x] T2 修复枚举大小写（color_type/price_type values_callable）
- [x] T3 修复 CORS_ORIGINS 解析（改 str + cors_origins_list 属性）
- [ ] T4 后端重启并验证 /api/quote/liandan 返回完整结构（含 ladder_prices、cost_breakdown、machine_info）
- [ ] T5 前端补 vue-router 配置（修复 router-view 白屏）+ 首页九宫格品类页 + 联单报价页路由
- [ ] T6 完善后端联单字段与逻辑：背面印刷、份数联动校验、自定义尺寸、多工序计价、利润率
- [ ] T7 前端联单页对齐参考站视觉（首页品类九宫格、面包屑、表单、结果区），原创资源
- [ ] T8 前后端联调，用 Playwright 浏览器验证完整报价流程与渲染
- [ ] T9 回归：标准案例计算、阶梯价、成本明细弹窗、币种/客户类型切换

## 运行方式
- 后端：`cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000`（开发期不加 --reload，子目录改动不被捕获）
- 前端：`cd frontend && npm run dev` → http://localhost:5173
- 数据库：MySQL80 服务，schema 在 database/schema.sql

## 已知坑
- uvicorn --reload 不监控 app/models 等子目录改动 → 改后端代码后手动重启进程。
- pydantic-settings 会把含逗号的 env 值当 JSON → 用 str 字段 + property 拆分。
- SQLAlchemy Enum 默认用成员名存取，需 values_callable 用 value。
