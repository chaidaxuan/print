-- 印刷「颜色加价模型」迁移脚本（对已存在的开发库执行一次）
-- 背景：schema.sql 用 CREATE TABLE IF NOT EXISTS，对已存在的 printing_colors 加列不生效，
--       故对现有库单独执行本迁移。补齐 11 种颜色 + 两列颜色加价增量 + 校准海德堡机器参数。
-- 用法：mysql -u root -p printing_quote < database/migration_color_fee_model.sql
--
-- 语义（yinshuabaojia.com 实测反标定，27 个数据点零误差）：
--   印刷费 = 单黑基准 + 颜色固定增量(fixed_fee) + 颜色印工增量(ink_per_thousand) × k
--   k = ⌈印张 ÷ 1000⌉（向上取整到“千印”）；单黑基准 = 开机费 + 千印价 × k（海德堡 60 + 20k）。
--   关键纠正：四色与双色同价（四色机一遍过机），旧“按色数线性”公式对四色多收；
--            专色才逐色线性叠加（每专色独立一遍）；彩色+专色封顶=4专色。
--   机器上的旧 color_fee 列作废（颜色加价改由颜色表承载），保留列不动以兼容。
USE printing_quote;

-- 1. 颜色表新增两列：颜色固定增量 + 颜色印工增量（相对单黑基准的加价）
--    注：不用 ADD COLUMN IF NOT EXISTS（仅 MySQL 8.0.29+/MariaDB 支持）；
--    列已存在时 runner 会捕获 1060 重复列错误并跳过，保持幂等。
ALTER TABLE printing_colors
    ADD COLUMN fixed_fee DECIMAL(10,2) DEFAULT 0
        COMMENT '颜色固定增量(元)：相对单黑基准的一次性加价' AFTER price_multiplier,
    ADD COLUMN ink_per_thousand DECIMAL(10,2) DEFAULT 0
        COMMENT '颜色印工增量(元/千印)：随印张(每千,向上取整)叠加的加价' AFTER fixed_fee;

-- 2. 重刷 11 种颜色（专版联单参考站口径）。先清旧 4 条再插，code 唯一键，硬删重插。
DELETE FROM printing_colors;
INSERT INTO printing_colors
    (name, code, plate_count, color_type, price_multiplier, fixed_fee, ink_per_thousand, sort_order) VALUES
('空白',        'blank',       0, 'black', 0,   0,   0,  1),
('单黑',        'single_black',1, 'black', 1.0, 0,   0,  2),
('双色',        'two_color',   2, 'spot',  1.5, 70,  0,  3),
('四色(彩色)',  'cmyk',        4, 'cmyk',  2.0, 70,  0,  4),
('1专色',       'spot_1',      1, 'spot',  1.0, 60,  10, 5),
('2专色',       'spot_2',      2, 'spot',  1.5, 100, 20, 6),
('3专色',       'spot_3',      3, 'spot',  2.0, 140, 30, 7),
('4专色',       'spot_4',      4, 'spot',  2.5, 180, 40, 8),
('彩色+1专色',  'cmyk_spot_1', 5, 'mixed', 2.5, 180, 40, 9),
('彩色+2专色',  'cmyk_spot_2', 6, 'mixed', 3.0, 180, 40, 10),
('彩色+3专色',  'cmyk_spot_3', 7, 'mixed', 3.0, 180, 40, 11),
('彩色+4专色',  'cmyk_spot_4', 8, 'mixed', 3.0, 180, 40, 12);

-- 3. 校准海德堡6开机器参数：开机费 60、千印价 20（实测 7 个数量点零误差）。
--    旧值(开机80/千印16.16 或 schema 里 150/80)在大数量会发散，此处统一为 60/20。
UPDATE printing_machines SET opening_fee = 60, price_per_thousand = 20 WHERE code = 'heidelberg_6k';
