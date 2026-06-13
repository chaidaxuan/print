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
    price_per_sheet DECIMAL(10,4) NOT NULL COMMENT '单张价格(元/张)',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_gram (gram_weight),
    INDEX idx_spec (spec_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='纸张规格与价格表';

-- 5. 后道工序价格表
CREATE TABLE IF NOT EXISTS post_processing (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL COMMENT '工序名称：装订-胶左、打号码',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '工序代码',
    category VARCHAR(50) COMMENT '工序分类',
    price_type ENUM('fixed', 'per_unit', 'per_thousand') DEFAULT 'per_unit' COMMENT '计价方式',
    unit_price DECIMAL(10,4) NOT NULL COMMENT '单价',
    min_charge DECIMAL(10,2) DEFAULT 0 COMMENT '最低收费',
    description TEXT COMMENT '工序说明',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='后道工序价格表';

-- 6. 印刷颜色配置表
CREATE TABLE IF NOT EXISTS printing_colors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL COMMENT '颜色名称：单黑、四色、双色',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '颜色代码',
    plate_count INT NOT NULL COMMENT '版数',
    color_type ENUM('black', 'spot', 'cmyk', 'mixed') COMMENT '颜色类型',
    price_multiplier DECIMAL(10,4) DEFAULT 1.0000 COMMENT '价格系数',
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
INSERT INTO printing_machines (name, code, max_width, max_height, machine_type, opening_fee, price_per_thousand) VALUES
('海德堡6开四色机', 'heidelberg_6k', 420, 285, '四色机', 150, 80),
('小森920B对开机', 'komori_920b', 920, 640, '对开机', 200, 100),
('小森1620全开机', 'komori_1620', 1600, 1200, '全开机', 300, 120),
('小森1320全开机', 'komori_1320', 1300, 900, '全开机', 250, 110);

-- 初始化纸张规格（无碳纸）
INSERT INTO paper_specs (name, category, gram_weight, width, height, spec_name, price_per_sheet) VALUES
('无碳纸', '无碳纸', 50, 889, 1194, '大度全开', 0.85),
('无碳纸', '无碳纸', 80, 889, 1194, '大度全开', 1.20),
('无碳纸', '无碳纸', 108, 889, 1194, '大度全开', 1.50);

-- 初始化后道工序
INSERT INTO post_processing (name, code, category, price_type, unit_price, description) VALUES
('装订-胶左', 'binding_left', '装订', 'per_unit', 0.20, '左侧胶装订'),
('装订-胶头', 'binding_top', '装订', 'per_unit', 0.20, '顶部胶装订'),
('打号码', 'numbering', '打码', 'per_unit', 0.05, '打印流水号'),
('压痕压点线', 'creasing', '压线', 'per_unit', 0.08, '压痕或压点线'),
('加封面', 'add_cover', '封面', 'per_unit', 0.15, '增加封面');

-- 初始化印刷颜色
INSERT INTO printing_colors (name, code, plate_count, color_type, price_multiplier, sort_order) VALUES
('空白', 'blank', 0, 'black', 0, 1),
('单黑', 'single_black', 1, 'black', 1.0, 2),
('双色', 'two_color', 2, 'spot', 1.5, 3),
('四色', 'cmyk', 4, 'cmyk', 2.0, 4);

-- 初始化系统参数
INSERT INTO system_params (param_key, param_value, param_type, description) VALUES
('cost_markup_rate', '0.609', 'cost_markup', '成本附加率（生产成本基础上的加成比例）'),
('wastage_rate', '0.05', 'wastage_rate', '印刷损耗率'),
('default_paper_loss', '10', 'wastage', '默认纸张损耗张数');
