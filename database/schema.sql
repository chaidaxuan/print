-- 印刷报价系统数据库设计
-- 基于无碳联单报价逻辑设计

-- 1. 产品品类表
CREATE TABLE IF NOT EXISTS product_categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '品类名称：无碳联单、彩盒、画册等',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '品类代码：liandan, caihe等',
    description TEXT COMMENT '品类描述',
    icon_url VARCHAR(255) COMMENT '图标URL',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品品类表';

-- 2. 成品尺寸规格表
CREATE TABLE IF NOT EXISTS product_sizes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL COMMENT '所属品类',
    name VARCHAR(50) NOT NULL COMMENT '尺寸名称：32开、A4等',
    width DECIMAL(10,2) NOT NULL COMMENT '宽度(mm)',
    height DECIMAL(10,2) NOT NULL COMMENT '高度(mm)',
    code VARCHAR(50) COMMENT '尺寸代码：32k、a4等',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (category_id) REFERENCES product_categories(id) ON DELETE CASCADE,
    INDEX idx_category (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成品尺寸规格表';

-- 3. 印刷机器参数表
CREATE TABLE IF NOT EXISTS printing_machines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '机器名称：海德堡6开四色机',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '机器代码',
    max_width DECIMAL(10,2) NOT NULL COMMENT '最大印刷宽度(mm)',
    max_height DECIMAL(10,2) NOT NULL COMMENT '最大印刷高度(mm)',
    machine_type VARCHAR(50) COMMENT '机型：四色、对开、全开',
    opening_fee DECIMAL(10,2) DEFAULT 0 COMMENT '开机费(元)',
    color_fee DECIMAL(10,2) DEFAULT 0 COMMENT '加色费(元/色，每加一色的开机加价)',
    price_per_thousand DECIMAL(10,2) DEFAULT 0 COMMENT '千印价(元/千张)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='印刷机器参数表';

-- 4. 纸张规格与价格表
CREATE TABLE IF NOT EXISTS paper_specs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '纸张名称：无碳纸、铜版纸',
    category VARCHAR(50) COMMENT '纸张分类',
    gram_weight INT NOT NULL COMMENT '克重(g)',
    width DECIMAL(10,2) COMMENT '纸张宽度(mm)',
    height DECIMAL(10,2) COMMENT '纸张高度(mm)',
    spec_name VARCHAR(50) COMMENT '规格名称：大度、正度',
    price_per_sheet DECIMAL(10,4) NOT NULL COMMENT '单张价格(元/张)，由令价换算，保留兼容',
    price_per_ream DECIMAL(10,2) COMMENT '令价(元/令，1令=500全张)，实测反推，报价按此换算单张',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_gram (gram_weight),
    INDEX idx_spec (spec_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='纸张规格与价格表';

-- 4.5 联单纸张分层价格表
-- 联单报价时，一本按联数分成"上/中/下"若干层，每层用不同纸价（上纸贵、下纸便宜）。
-- 数据库存的是令价（元/令），计算时先转吨价，再按页数逐层加权求和。
-- 令价→吨价公式：吨价 = 令价 × 1,000,000 ÷ (克重 × 单张面积 × 500)
--   单张面积：大度 1.06 m²、正度 0.86 m²（即纸张系数）。
-- 层价回退：某层令价为 0 时，依次回退 中→上→下，都为 0 用默认吨价（大度8000、正度7000）。
CREATE TABLE IF NOT EXISTS union_paper_prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    weight INT NOT NULL COMMENT '纸张克重(g)',
    dadu_upper_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '大度上纸令价(元/令)',
    dadu_middle_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '大度中纸令价(元/令)',
    dadu_lower_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '大度下纸令价(元/令)',
    zhengdu_upper_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '正度上纸令价(元/令)',
    zhengdu_middle_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '正度中纸令价(元/令)',
    zhengdu_lower_price DECIMAL(10,2) NOT NULL DEFAULT 0 COMMENT '正度下纸令价(元/令)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_weight (weight)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='联单纸张分层价格表';

-- 5. 后道工序价格表
-- 计价单位对齐参考站：元/本(per_book)、元/版(per_plate)、元/页(per_page)、元/联(per_sheet_count)。
-- 加卡纸/装订按成品开数分多档：每档一条独立记录(code=binding_1..4)，group_code(binding)串同组，
-- 引擎按 group_code + 成品开数(kai) 选档，见 quote_engine._resolve_processing。
CREATE TABLE IF NOT EXISTS post_processing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '工序名称：装订(20开-50开)、彩色联单加号码',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '工序代码，全表唯一',
    category VARCHAR(50) COMMENT '工序分类',
    price_type ENUM('fixed', 'per_unit', 'per_thousand', 'per_book', 'per_plate', 'per_page', 'per_sheet_count') DEFAULT 'per_book' COMMENT '计价方式',
    unit_price DECIMAL(10,4) NOT NULL COMMENT '单价',
    min_charge DECIMAL(10,2) DEFAULT 0 COMMENT '最低收费(最低消费/开机费)',
    group_code VARCHAR(50) COMMENT '前端勾选分组，如 add_card/binding；单档项即 code',
    min_kai INT COMMENT '开数档下限(含)，仅展示；NULL=不限',
    max_kai INT COMMENT '开数档上限(含)，选档用；NULL=最大档(如50开以上)',
    sort_order INT DEFAULT 0 COMMENT '展示排序',
    description TEXT COMMENT '工序说明',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_group (group_code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后道工序价格表';

-- 6. 印刷颜色配置表
CREATE TABLE IF NOT EXISTS printing_colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '颜色名称：单黑、四色、双色',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '颜色代码',
    plate_count INT NOT NULL COMMENT '色数（单黑1/双色2/四色4/N专色N/彩色+专色5+），0=空白免印',
    color_type ENUM('black', 'spot', 'cmyk', 'mixed') COMMENT '颜色类型',
    price_multiplier DECIMAL(10,4) DEFAULT 1.0000 COMMENT '价格系数（旧字段，保留兼容，现已不参与印刷费计算）',
    fixed_fee DECIMAL(10,2) DEFAULT 0 COMMENT '颜色固定增量(元)：相对单黑基准的额外固定开机费',
    ink_per_thousand DECIMAL(10,2) DEFAULT 0 COMMENT '颜色印工增量(元/千印)：相对单黑基准每千印张的额外印工',
    sort_order INT DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='印刷颜色配置表';

-- 7. 系统参数配置表
CREATE TABLE IF NOT EXISTS system_params (
    id INT AUTO_INCREMENT PRIMARY KEY,
    param_key VARCHAR(100) NOT NULL UNIQUE COMMENT '参数键',
    param_value TEXT NOT NULL COMMENT '参数值(JSON格式)',
    param_type VARCHAR(50) COMMENT '参数类型：cost_markup成本附加、wastage_rate损耗率',
    description TEXT COMMENT '参数说明',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统参数配置表';

-- 8. 报价记录表
CREATE TABLE IF NOT EXISTS quote_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL COMMENT '品类ID',
    quote_no VARCHAR(50) UNIQUE COMMENT '报价单号',
    customer_name VARCHAR(100) COMMENT '客户名称',
    product_name VARCHAR(200) COMMENT '产品名称',

    -- 无碳联单参数（JSON存储，方便扩展到其他品类）
    form_data JSON COMMENT '表单参数',

    -- 计算结果
    cost_breakdown JSON COMMENT '成本明细',
    unit_price DECIMAL(10,4) COMMENT '单价',
    total_price DECIMAL(10,2) COMMENT '总价',
    quantity INT COMMENT '数量',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_category (category_id),
    INDEX idx_created (created_at),
    FOREIGN KEY (category_id) REFERENCES product_categories(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='报价记录表';

-- 初始化产品品类
INSERT INTO product_categories (name, code, description, sort_order) VALUES
('无碳联单', 'liandan', '专版联单报价，支持多联、自定义尺寸、多种印刷颜色', 1);

-- 初始化成品尺寸（无碳联单）
INSERT INTO product_sizes (category_id, name, width, height, code, sort_order) VALUES
(1, '32开 210×140 A5', 210, 140, '32k', 1),
(1, '16开 210×285 A4', 210, 285, '16k', 2),
(1, '8开 420×285 A3', 420, 285, '8k', 3),
(1, '64开 105×145 A6', 105, 145, '64k', 4),
(1, '48开 210×95', 210, 95, '48k', 5);

-- 初始化印刷机器
-- opening_fee=开机费、price_per_thousand=千印价(元/千印，印工按 ⌈印张/1000⌉ 整千计)。
-- 海德堡6开由 yinshuabaojia.com 实测反标定：单黑印刷费 = 60 + 20×⌈印张/1000⌉
--   （7 个数量点 100~5000 零误差）。旧值 150/80 及会被本次覆盖的 80/16.16 均会在大数量发散。
-- color_fee 列已弃用：颜色加价改由 printing_colors.fixed_fee / ink_per_thousand 承载（见颜色 seed）。
INSERT INTO printing_machines (name, code, max_width, max_height, machine_type, opening_fee, price_per_thousand, color_fee) VALUES
('海德堡6开四色机', 'heidelberg_6k', 460, 320, '四色机', 60, 20, 0),
('小森920B对开机', 'komori_920b', 920, 640, '对开机', 200, 100, 0),
('小森1620全开机', 'komori_1620', 1600, 1200, '全开机', 300, 120, 0),
('小森1320全开机', 'komori_1320', 1300, 900, '全开机', 250, 110, 0);

-- 初始化纸张规格（无碳纸）
-- price_per_ream 令价(元/令，1令=500全张)为主计价，price_per_sheet=令价/500 兜底。
-- 50克令价 394 由 yinshuabaojia.com 实测反推(100本纸款254、买纸322全张 → 254/322×500≈394)。
INSERT INTO paper_specs (name, category, gram_weight, width, height, spec_name, price_per_ream, price_per_sheet) VALUES
('无碳纸', '无碳纸', 50, 889, 1194, '大度全开', 394, 0.788),
('无碳纸', '无碳纸', 80, 889, 1194, '大度全开', 577, 1.154),
('无碳纸', '无碳纸', 108, 889, 1194, '大度全开', 721, 1.442);

-- 初始化联单分层纸价（大度/正度 × 上中下，令价 元/令）
-- 占位值基于 paper_specs 令价分层：上纸 +5%、中纸基准、下纸 -5%（后续可按实测校准）。
-- 大度基准取 paper_specs.price_per_ream；正度暂按大度 ×0.81（正度面积≈0.86/1.06≈0.81 大度）。
INSERT INTO union_paper_prices (weight, dadu_upper_price, dadu_middle_price, dadu_lower_price, zhengdu_upper_price, zhengdu_middle_price, zhengdu_lower_price) VALUES
(50,  414, 394, 374,  335, 319, 303),
(80,  606, 577, 548,  491, 467, 444),
(108, 757, 721, 685,  613, 584, 555);

-- 初始化后道工序（对齐 yinshuabaojia.com 参考站后工参数表）
-- 加卡纸、装订按成品开数分4档；其余为单档。min_kai 仅展示，选档以 max_kai 为准
-- （升序取第一个 max_kai>=成品开数的档，NULL 为“50开以上”兜底档）。
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

-- 初始化印刷颜色（含颜色对印刷费的增量：fixed_fee 固定增量、ink_per_thousand 每千印张印工增量）
--   印刷费 = 单黑基准(开机+千印价×k) + fixed_fee + ink_per_thousand×k，k=⌈印张/1000⌉。
--   参考站 yinshuabaojia 演示反标定，27 个数据点(9色×3数量)零误差：
--     双色/四色同价(四色机一遍过机)；N专色每色独立一遍(开机+40、印工+10k)；彩色+专色封顶=4专色。
INSERT INTO printing_colors (name, code, plate_count, color_type, price_multiplier, fixed_fee, ink_per_thousand, sort_order) VALUES
('空白',        'blank',        0, 'black', 0,   0,   0,  1),
('单黑',        'single_black', 1, 'black', 1.0, 0,   0,  2),
('双色',        'two_color',    2, 'spot',  1.5, 70,  0,  3),
('四色(彩色)',   'cmyk',         4, 'cmyk',  2.0, 70,  0,  4),
('1专色',       'spot_1',       1, 'spot',  1.0, 60,  10, 5),
('2专色',       'spot_2',       2, 'spot',  1.0, 100, 20, 6),
('3专色',       'spot_3',       3, 'spot',  1.0, 140, 30, 7),
('4专色',       'spot_4',       4, 'spot',  1.0, 180, 40, 8),
('彩色+1专色',   'cmyk_spot_1',  5, 'mixed', 1.0, 180, 40, 9),
('彩色+2专色',   'cmyk_spot_2',  6, 'mixed', 1.0, 180, 40, 10),
('彩色+3专色',   'cmyk_spot_3',  7, 'mixed', 1.0, 180, 40, 11),
('彩色+4专色',   'cmyk_spot_4',  8, 'mixed', 1.0, 180, 40, 12);

-- 初始化系统参数
INSERT INTO system_params (param_key, param_value, param_type, description) VALUES
('cost_markup_rate', '0.609', 'cost_markup', '成本附加率（生产成本基础上的加成比例，已弃用，改由 cost_addon_tiers 阶梯表驱动）'),
('wastage_rate', '0.05', 'wastage_rate', '印刷损耗率'),
('default_paper_loss', '100', 'wastage', '默认纸张损耗张数(印张层级放数)');

-- 9. 成本附加阶梯表
-- 依据 yinshuabaojia.com 专版联单实测反推：成本附加 = 生产成本 × 阶梯费率，
-- 费率随生产成本金额递增而递减，最低档 10% 封底（详见 docs/LIANDAN_CALC_LOGIC.md）。
CREATE TABLE IF NOT EXISTS cost_addon_tiers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL COMMENT '所属品类',
    min_cost DECIMAL(12,2) NOT NULL COMMENT '生产成本下限(含)',
    max_cost DECIMAL(12,2) COMMENT '生产成本上限(不含)，NULL 表示无上限',
    rate DECIMAL(6,4) NOT NULL COMMENT '该档费率(小数，如0.609)',
    fixed_addon DECIMAL(10,2) DEFAULT 0 COMMENT '该档固定附加值(元)，实测为0，保留以兼容真实参数',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category_id),
    FOREIGN KEY (category_id) REFERENCES product_categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='成本附加阶梯表';

-- 初始化成本附加阶梯（品类1=无碳联单）
-- 实测锚点：394→60.9%、675→39.7%、1247→22.1%、2713→15.6%、≥3090→10%封底。
-- 区间边界取相邻锚点的近似分界，上线前需接入真实 Tab5 参数校准。
INSERT INTO cost_addon_tiers (category_id, min_cost, max_cost, rate, fixed_addon, sort_order) VALUES
(1, 0,    500,  0.6090, 0, 1),
(1, 500,  1000, 0.3970, 0, 2),
(1, 1000, 1500, 0.2210, 0, 3),
(1, 1500, 3000, 0.1560, 0, 4),
(1, 3000, NULL, 0.1000, 0, 5);
