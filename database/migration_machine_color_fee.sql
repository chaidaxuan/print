-- 印刷机「加色费」迁移脚本（对已存在的开发库执行一次）
-- 背景：schema.sql 用 CREATE TABLE IF NOT EXISTS，对已存在的 printing_machines 加列不生效，
--       故对现有库单独执行本迁移。只加一列 + 回填海德堡，不动其它数据。
-- 用法：mysql -u root -p printing_quote < database/migration_machine_color_fee.sql
--
-- 语义：印刷费从旧的「版数 ×(开机+印工)」改为「开机 + 加色费×(色数-1) + 印工×色数」。
--       color.plate_count 实为色数(单黑1/双色2/四色4)。每加一色 = 加色费 color_fee + 一遍印工。
--       实测(海德堡6开)：单黑 80+40=120、双色 80+30+40×2=190，均命中参考站。
USE printing_quote;

-- 1. 新增加色费列（IF NOT EXISTS 需 MySQL 8.0+；老版本若报重复列可手动跳过）
ALTER TABLE printing_machines
    ADD COLUMN IF NOT EXISTS color_fee DECIMAL(10,2) DEFAULT 0 COMMENT '每加一色的加色开机费(元)'
    AFTER opening_fee;

-- 2. 回填：海德堡6开 30，其余机器暂 0（真实报价前在参数页按实际工价改）
UPDATE printing_machines SET color_fee = 30 WHERE code = 'heidelberg_6k';
