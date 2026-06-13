from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Text, Enum, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base
import enum


class PriceType(str, enum.Enum):
    """计价方式枚举"""
    FIXED = "fixed"
    PER_UNIT = "per_unit"
    PER_THOUSAND = "per_thousand"


class PostProcessing(Base):
    """后道工序价格模型"""

    __tablename__ = "post_processing"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="工序名称")
    code = Column(String(50), nullable=False, unique=True, comment="工序代码")
    category = Column(String(50), comment="工序分类")
    price_type = Column(
        Enum(PriceType, values_callable=lambda x: [e.value for e in x]),
        default=PriceType.PER_UNIT,
        comment="计价方式",
    )
    unit_price = Column(DECIMAL(10, 4), nullable=False, comment="单价")
    min_charge = Column(DECIMAL(10, 2), default=0, comment="最低收费")
    description = Column(Text, comment="工序说明")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
