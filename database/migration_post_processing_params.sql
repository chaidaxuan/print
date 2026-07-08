-- 后工参数闭环迁移脚本（对已存在的开发库执行一次）
-- 背景：schema.sql 用 CREATE TABLE IF NOT EXISTS，对已存在的 post_processing 改列不生效，
--       故对现有库单独执行本迁移。只动 post_processing 表，不 DROP 库，保住 quote_records 历史。
-- 用法：mysql -u root -p printing_quote < database/migration_post_processing_params.sql
USE printing_quote;

-- 1. 扩展计价单位枚举
ALTER TABLE post_processing
    MODIFY price_type ENUM('fixed', 'per_unit', 'per_thousand', 'per_book', 'per_plate', 'per_page', 'per_sheet_count')
    DEFAULT 'per_book' COMMENT '计价方式';

-- 2. 新增分档/展示所需列（IF NOT EXISTS 需 MySQL 8.0+；老版本若报重复列可手动跳过已存在的）
ALTER TABLE post_processing
    ADD COLUMN IF NOT EXISTS group_code VARCHAR(50) COMMENT '前端勾选分组，如 add_card/binding；单档项即 code',
    ADD COLUMN IF NOT EXISTS min_kai INT COMMENT '开数档下限(含)，仅展示；NULL=不限',
    ADD COLUMN IF NOT EXISTS max_kai INT COMMENT '开数档上限(含)，选档用；NULL=最大档(如50开以上)',
    ADD COLUMN IF NOT EXISTS sort_order INT DEFAULT 0 COMMENT '展示排序';

-- 3. group_code 索引（若已存在会报错，可忽略）
ALTER TABLE post_processing ADD INDEX idx_group (group_code);

-- 4. 清空旧工序，重灌参考站 13 行（整表覆盖语义）
DELETE FROM post_processing;
INSERT INTO post_processing (name, code, group_code, price_type, unit_price, min_charge, min_kai, max_kai, sort_order) VALUES
('加卡纸(10开-8开)',  'add_card_1',  'add_card',   'per_book',        0.4,  30, 1,    10,   1),
('加卡纸(11开-18开)', 'add_card_2',  'add_card',   'per_book',        0.2,  30, 11,   18,   2),
('加卡纸(20开-50开)', 'add_card_3',  'add_card',   'per_book',        0.2,  30, 19,   50,   3),
('加卡纸(50开以上)',  'add_card_4',  'add_card',   'per_book',        0.2,  30, 51,   NULL, 4),
('加封面',           'add_cover',   'add_cover',  'per_book',        0.3,  30, NULL, NULL, 5),
('印封面',           'print_cover', 'print_cover','per_book',        0.3,  30, NULL, NULL, 6),
('压点线',           'creasing',    'creasing',   'per_plate',       0.01, 30, NULL, NULL, 7),
('彩色联单加号码',    'numbering',   'numbering',  'per_page',        0.02, 0,  NULL, NULL, 8),
('装订(10开-8开)',   'binding_1',   'binding',    'per_book',        0.3,  20, 1,    10,   9),
('装订(11开-18开)',  'binding_2',   'binding',    'per_book',        0.3,  20, 11,   18,   10),
('装订(20开-50开)',  'binding_3',   'binding',    'per_book',        0.1,  20, 19,   50,   11),
('装订(50开以上)',   'binding_4',   'binding',    'per_book',        0.1,  20, 51,   NULL, 12),
('换边联字',         'edge_words',  'edge_words', 'per_sheet_count', 10,   30, NULL, NULL, 13);
