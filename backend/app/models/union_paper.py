"""联单纸张分层价格模型"""
from sqlalchemy import Column, Integer, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class UnionPaperPrice(Base):
    """联单纸张分层价格配置模型

    联单报价时，一本按联数分成"上/中/下"若干层，每层用不同纸价：
    - 上纸：最贵（显色好、耐用）
    - 中纸：基准价
    - 下纸：最便宜（存根联）

    数据库存的是令价（元/令），计算时先转吨价，再按页数逐层加权求和。
    """

    __tablename__ = "union_paper_prices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    weight = Column(Integer, nullable=False, unique=True, comment="纸张克重(g)")

    # 大度纸张价格（元/令）
    dadu_upper_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="大度上纸令价")
    dadu_middle_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="大度中纸令价")
    dadu_lower_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="大度下纸令价")

    # 正度纸张价格（元/令）
    zhengdu_upper_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="正度上纸令价")
    zhengdu_middle_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="正度中纸令价")
    zhengdu_lower_price = Column(DECIMAL(10, 2), nullable=False, default=0, comment="正度下纸令价")

    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
