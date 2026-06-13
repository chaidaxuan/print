from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Enum
from app.database import Base
import enum


class ColorType(str, enum.Enum):
    """颜色类型枚举"""
    BLACK = "black"
    SPOT = "spot"
    CMYK = "cmyk"
    MIXED = "mixed"


class PrintingColor(Base):
    """印刷颜色配置模型"""

    __tablename__ = "printing_colors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="颜色名称")
    code = Column(String(50), nullable=False, unique=True, comment="颜色代码")
    plate_count = Column(Integer, nullable=False, comment="版数")
    color_type = Column(
        Enum(ColorType, values_callable=lambda x: [e.value for e in x]),
        comment="颜色类型",
    )
    price_multiplier = Column(DECIMAL(10, 4), default=1.0, comment="价格系数")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
