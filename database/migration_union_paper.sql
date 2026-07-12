-- 联单纸张分层价格表迁移脚本（对已存在的开发库执行一次）
-- 背景：新增 union_paper_prices 表，支持联单"上中下纸"分层计价。
-- 用法：mysql -u root -p printing_quote < database/migration_union_paper.sql
--   或：python scripts/run_migration.py database/migration_union_paper.sql
--
-- 语义：联单报价时，一本按联数分成"上/中/下"若干层，每层用不同纸价（上纸贵、下纸便宜）。
--   数据库存令价（元/令），计算时转吨价，按页数逐层加权求和。
--   令价→吨价：吨价 = 令价 × 1,000,000 ÷ (克重 × 单张面积 × 500)
--   单张面积：大度 1.06 m²、正度 0.86 m²。
USE printing_quote;

-- 1. 新建联单分层纸价表
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

-- 2. 初始化分层纸价数据（大度/正度 × 上中下，令价 元/令）
-- 50g: 参考站实测不分层(统一394.41)，精确命中参考站纸款254。
-- 80g/108g: 上+5%、中=paper_specs基准令价、下-5%（待实测校准）。
-- 正度按大度 ×0.81 估算。
INSERT INTO union_paper_prices
    (weight, dadu_upper_price, dadu_middle_price, dadu_lower_price, zhengdu_upper_price, zhengdu_middle_price, zhengdu_lower_price)
VALUES
    (50,  394.41, 394.41, 394.41,  319.47, 319.47, 319.47),
    (80,  606.95, 578.05, 549.15,  491.63, 468.22, 444.81),
    (108, 758.69, 722.56, 686.43,  614.54, 585.27, 556.01)
ON DUPLICATE KEY UPDATE
    dadu_upper_price=VALUES(dadu_upper_price),
    dadu_middle_price=VALUES(dadu_middle_price),
    dadu_lower_price=VALUES(dadu_lower_price),
    zhengdu_upper_price=VALUES(zhengdu_upper_price),
    zhengdu_middle_price=VALUES(zhengdu_middle_price),
    zhengdu_lower_price=VALUES(zhengdu_lower_price);
