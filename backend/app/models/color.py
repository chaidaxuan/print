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
    # —— 颜色对印刷费的增量（相对单黑基准；机器无关，实测反标定）——
    #   印刷费 = 单黑基准(开机+千印价×k) + fixed_fee + ink_per_thousand × k
    #   k = ⌈印张/1000⌉。空白免印两项皆 0。双色/四色 fixed=70/ink=0（一遍过机、同价）；
    #   N专色 fixed=20+40N、ink=10N（各自独立一遍）；彩色+专色封顶=4专色。
    fixed_fee = Column(DECIMAL(10, 2), default=0, comment="颜色固定加价(元，相对单黑)")
    ink_per_thousand = Column(DECIMAL(10, 2), default=0, comment="颜色印工加价(元/千印张，相对单黑)")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
