from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class PaperSpec(Base):
    """纸张规格与价格模型"""

    __tablename__ = "paper_specs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="纸张名称")
    category = Column(String(50), comment="纸张分类")
    gram_weight = Column(Integer, nullable=False, index=True, comment="克重")
    width = Column(DECIMAL(10, 2), comment="纸张宽度(mm)")
    height = Column(DECIMAL(10, 2), comment="纸张高度(mm)")
    spec_name = Column(String(50), index=True, comment="规格名称")
    price_per_sheet = Column(DECIMAL(10, 4), nullable=False, comment="单张价格(元/张，由令价/500换算，保留兼容)")
    price_per_ream = Column(DECIMAL(10, 2), comment="令价(元/令，1令=500全张)，实测反推的真实计价口径")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
