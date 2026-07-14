-- 专版画册报价 — 数据库迁移脚本（对已存在的开发库执行一次）
-- 用法：python scripts/run_migration.py database/migration_huace.sql
--
-- 计算模型来源：直接调用参考站 yinshuabaojia.com 演示号265 的
--   /ashx/YouXiaoQuotePrice.ashx 接口做参数扫描逆向，已验算到元。
--   详见 memory/huace-calc-logic.md。
--
-- 基准（大度16开285×210，封面双铜80克/4P/四色双面，内页1 双铜80克/16P/四色，1000本）：
--   纸款771 + 印刷1250 + 表面处理102 + 骑马钉100 = 成本2223，单价2.223。
--   成本价即生产成本（画册无成本附加），各客户类型价 = 成本价 × 客户倍率。
USE printing_quote;

-- ============================================================
-- 1. 品类：专版画册（用 code='huace' 幂等）
-- ============================================================
INSERT INTO product_categories (name, code, description, sort_order, is_active)
VALUES ('专版画册', 'huace', '封面+内页画册，按吨计价、按版数计印刷费', 2, TRUE)
ON DUPLICATE KEY UPDATE name=VALUES(name), description=VALUES(description);

SET @huace_id = (SELECT id FROM product_categories WHERE code='huace');

-- ============================================================
-- 2. 成品尺寸（画册常用开数；kai 记录成品开数，用于拼版）
-- ============================================================
DELETE FROM product_sizes WHERE category_id=@huace_id;
INSERT INTO product_sizes (category_id, name, width, height, code, sort_order, is_active)
VALUES
    (@huace_id, '大度16开(285×210)A4', 285, 210, 'dadu_16k', 1, TRUE),
    (@huace_id, '大度32开(210×142)A5', 210, 142, 'dadu_32k', 2, TRUE),
    (@huace_id, '大度8开(420×285)A3',  420, 285, 'dadu_8k',  3, TRUE),
    (@huace_id, '正度16开(260×185)',   260, 185, 'zhengdu_16k', 4, TRUE),
    (@huace_id, '正度32开(185×130)',   185, 130, 'zhengdu_32k', 5, TRUE);

-- ============================================================
-- 3. 画册纸张（按吨计价）
--    ton_price=元/吨；full_area 由尺寸的大度/正度推断（引擎内定）。
--    数据取自参考站封面/内页纸张下拉：常用纸类×(双铜/双胶/白牛卡)×克重。
-- ============================================================
CREATE TABLE IF NOT EXISTS huace_paper_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_category VARCHAR(50) NOT NULL COMMENT '纸类：常用纸类/UV印刷类/PVC胶片',
    paper_name VARCHAR(50) NOT NULL COMMENT '纸名：双铜纸/双胶纸/双面白牛卡',
    weight INT NOT NULL COMMENT '克重(g)',
    ton_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '吨价(元/吨)',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_huace_paper (paper_category, paper_name, weight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='画册纸张吨价表';

DELETE FROM huace_paper_prices;
INSERT INTO huace_paper_prices (paper_category, paper_name, weight, ton_price, sort_order) VALUES
    ('常用纸类', '双铜纸', 80,  12800, 1),
    ('常用纸类', '双铜纸', 105, 12800, 2),
    ('常用纸类', '双铜纸', 116, 9000,  3),
    ('常用纸类', '双铜纸', 128, 12400, 4),
    ('常用纸类', '双铜纸', 140, 12000, 5),
    ('常用纸类', '双铜纸', 150, 12000, 6),
    ('常用纸类', '双铜纸', 157, 12000, 7),
    ('常用纸类', '双铜纸', 200, 12000, 8),
    ('常用纸类', '双铜纸', 250, 12000, 9),
    ('常用纸类', '双铜纸', 300, 12000, 10),
    ('常用纸类', '双铜纸', 350, 12000, 11),
    ('常用纸类', '双胶纸', 70,  11000, 20),
    ('常用纸类', '双胶纸', 80,  11000, 21),
    ('常用纸类', '双胶纸', 100, 11000, 22),
    ('常用纸类', '双胶纸', 120, 11000, 23),
    ('常用纸类', '双面白牛卡', 250, 9500, 30),
    ('常用纸类', '双面白牛卡', 300, 9500, 31),
    ('常用纸类', '双面白牛卡', 350, 9500, 32);

-- ============================================================
-- 4. 画册印刷色价（每版价，按 部件×颜色 查表）
--    版数：封面自反版=1；内页=P×4÷成品开数(kai)。印刷费=版数×每版价。
--    实测反推（四开机）：
--      封面 单黑100/双色200/四色250（自反，正反同版）
--      内页 单黑75/双色150/四色250（每版）
-- ============================================================
CREATE TABLE IF NOT EXISTS huace_color_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    component VARCHAR(20) NOT NULL COMMENT '部件：cover(封面)/inner(内页)',
    color_code VARCHAR(30) NOT NULL COMMENT '颜色代码',
    color_name VARCHAR(50) NOT NULL COMMENT '颜色名称',
    price_per_version DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '每版价(元/版)',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_huace_color (component, color_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='画册印刷色价表(每版)';

DELETE FROM huace_color_prices;
INSERT INTO huace_color_prices (component, color_code, color_name, price_per_version, sort_order) VALUES
    -- 封面（自反版，版数=1）
    ('cover', 'blank',        '空白',       0,   1),
    ('cover', 'single_black', '单黑',       100, 2),
    ('cover', 'double',       '双色',       200, 3),
    ('cover', 'cmyk',         '四色(彩色)', 250, 4),
    ('cover', 'spot1',        '1专色',      100, 5),
    ('cover', 'spot2',        '2专色',      200, 6),
    ('cover', 'spot3',        '3专色',      250, 7),
    ('cover', 'spot4',        '4专色',      250, 8),
    ('cover', 'cmyk_spot1',   '彩色+1专色', 350, 9),
    ('cover', 'cmyk_spot2',   '彩色+2专色', 450, 10),
    ('cover', 'cmyk_spot3',   '彩色+3专色', 550, 11),
    ('cover', 'cmyk_spot4',   '彩色+4专色', 650, 12),
    -- 内页（每版价）
    ('inner', 'blank',        '空白',       0,   1),
    ('inner', 'single_black', '单黑',       75,  2),
    ('inner', 'double',       '双色',       150, 3),
    ('inner', 'cmyk',         '四色(彩色)', 250, 4),
    ('inner', 'spot1',        '1专色',      75,  5),
    ('inner', 'spot2',        '2专色',      150, 6),
    ('inner', 'spot3',        '3专色',      225, 7),
    ('inner', 'spot4',        '4专色',      250, 8),
    ('inner', 'cmyk_spot1',   '彩色+1专色', 325, 9),
    ('inner', 'cmyk_spot2',   '彩色+2专色', 400, 10),
    ('inner', 'cmyk_spot3',   '彩色+3专色', 475, 11),
    ('inner', 'cmyk_spot4',   '彩色+4专色', 550, 12);

-- ============================================================
-- 5. 装订方式（8 种；price_type=per_book 元/本）
--    骑马钉实测 0.1元/本；其余为初始估值，测试阶段对拍校准。
-- ============================================================
CREATE TABLE IF NOT EXISTS huace_binding (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(30) NOT NULL COMMENT '装订代码',
    name VARCHAR(50) NOT NULL COMMENT '装订名称',
    price_type VARCHAR(20) NOT NULL DEFAULT 'per_book' COMMENT '计价单位',
    unit_price DECIMAL(10,4) NOT NULL DEFAULT 0 COMMENT '单价',
    min_charge DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '最低消费',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_huace_binding (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='画册装订方式表';

DELETE FROM huace_binding;
INSERT INTO huace_binding (code, name, price_type, unit_price, min_charge, sort_order) VALUES
    ('saddle_stitch', '骑马钉',      'per_book', 0.10, 0,   1),
    ('sewn',          '车线本',      'per_book', 0.30, 100, 2),
    ('perfect',       '无线胶装',    'per_book', 0.35, 150, 3),
    ('sewn_perfect',  '锁线胶装',    'per_book', 0.50, 200, 4),
    ('hard_self',     '精装(自衬)',  'per_book', 2.50, 300, 5),
    ('hard_ring',     '精装(环衬)',  'per_book', 3.00, 300, 6),
    ('yo',            'YO圈装',      'per_book', 0.80, 150, 7),
    ('notebook',      '笔记本',      'per_book', 1.00, 150, 8);

-- ============================================================
-- 6. 后道工序（表面处理 + 其他工序）
--    表面处理按封面印张面积计价：max(封面买纸数 × 全开面积 × 单价, 最低消费)。
--    单价取自参考站表面处理下拉（元/…）。
-- ============================================================
CREATE TABLE IF NOT EXISTS huace_post_processing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(40) NOT NULL COMMENT '工序代码',
    name VARCHAR(50) NOT NULL COMMENT '工序名称',
    proc_group VARCHAR(30) NOT NULL COMMENT '分组：surface(表面处理)/other(其他)',
    price_type VARCHAR(20) NOT NULL DEFAULT 'per_area' COMMENT '计价：per_area(元/㎡印张)/per_book/fixed',
    unit_price DECIMAL(10,4) NOT NULL DEFAULT 0 COMMENT '单价',
    min_charge DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '最低消费',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_huace_post (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='画册后道工序表';

DELETE FROM huace_post_processing;
INSERT INTO huace_post_processing (code, name, proc_group, price_type, unit_price, min_charge, sort_order) VALUES
    ('film_gloss',    '过光膜',       'surface', 'per_area', 0.40, 100, 1),
    ('film_matte',    '过哑膜',       'surface', 'per_area', 0.45, 100, 2),
    ('film_scratch',  '防刮花膜',     'surface', 'per_area', 0.60, 100, 3),
    ('film_super',    '过超感膜',     'surface', 'per_area', 1.00, 100, 4),
    ('film_laser',    '过镭射膜',     'surface', 'per_area', 0.60, 100, 5),
    ('oil_gloss',     '过光油',       'surface', 'per_area', 0.20, 80,  6),
    ('oil_matte',     '过哑油',       'surface', 'per_area', 0.25, 80,  7),
    ('oil_blister',   '过吸塑油',     'surface', 'per_area', 0.30, 80,  8),
    ('polish',        '磨光',         'surface', 'per_area', 0.30, 80,  9),
    ('polish_blister','磨光吸塑',     'surface', 'per_area', 0.35, 80,  10),
    ('uv_oil_gloss',  '满版UV光油',   'surface', 'per_area', 0.45, 100, 11),
    ('uv_oil_matte',  '满版UV哑油',   'surface', 'per_area', 0.45, 100, 12),
    ('uv_frosted',    '满版UV磨砂',   'surface', 'per_area', 0.45, 100, 13),
    ('film_window',   '开窗过光膜',   'surface', 'per_area', 0.60, 120, 14),
    ('die_cut',       '模切',         'other',   'per_book', 0.05, 100, 30),
    ('emboss_pattern','压纹',         'other',   'per_book', 0.05, 100, 31),
    ('flap_cover',    '封面加勒口',   'other',   'per_book', 0.10, 100, 32),
    ('flap_back',     '封底加勒口',   'other',   'per_book', 0.10, 100, 33),
    ('bump',          '击凸',         'other',   'per_book', 0.08, 120, 34),
    ('debump',        '击凹',         'other',   'per_book', 0.08, 120, 35),
    ('round_corner',  '切圆角',       'other',   'per_book', 0.03, 60,  36),
    ('pack',          '打包',         'other',   'fixed',    0,    50,  37);

-- ============================================================
-- 7. 客户加价倍率（对成本价 GroupId=-1）
-- ============================================================
CREATE TABLE IF NOT EXISTS huace_client_tiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(30) NOT NULL COMMENT '客户类型代码',
    name VARCHAR(50) NOT NULL COMMENT '客户类型名称',
    multiplier DECIMAL(6,4) NOT NULL DEFAULT 1 COMMENT '相对成本价倍率',
    remark VARCHAR(200) COMMENT '备注',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_huace_client (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='画册客户加价倍率表';

DELETE FROM huace_client_tiers;
INSERT INTO huace_client_tiers (code, name, multiplier, remark, sort_order) VALUES
    ('cost',        '成本价',      1.0000, '直接计算出来的成本', 1),
    ('cash',        '现金客户',    1.1500, '现金客户，不含运费，不含税。', 2),
    ('cash_invoice','现金开票客户',1.3000, '现金客户，不含运费，13点增值税。', 3),
    ('month30',     '30天月结客户',1.2500, '月结客户，不含运费，不含税。', 4),
    ('agent',       '中介客户',    1.1000, '现金客户，不含运费，不含税。', 5),
    ('month_invoice','月结开票客户',1.4000,'月结客户，不含运费，13点增值税。', 6);
