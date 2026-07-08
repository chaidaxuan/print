from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class PrintingMachine(Base):
    """印刷机器参数模型"""

    __tablename__ = "printing_machines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, comment="机器名称")
    code = Column(String(50), nullable=False, unique=True, comment="机器代码")
    max_width = Column(DECIMAL(10, 2), nullable=False, comment="最大印刷宽度(mm)")
    max_height = Column(DECIMAL(10, 2), nullable=False, comment="最大印刷高度(mm)")
    machine_type = Column(String(50), comment="机型")
    opening_fee = Column(DECIMAL(10, 2), default=0, comment="开机费(元)")
    color_fee = Column(DECIMAL(10, 2), default=0, comment="加色费(元/色，每加一色的额外开机费)")
    price_per_thousand = Column(DECIMAL(10, 2), default=0, comment="千印价(元/千张)")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
