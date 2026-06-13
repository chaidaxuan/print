from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class SystemParam(Base):
    """系统参数配置模型"""

    __tablename__ = "system_params"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    param_key = Column(String(100), nullable=False, unique=True, comment="参数键")
    param_value = Column(Text, nullable=False, comment="参数值(JSON格式)")
    param_type = Column(String(50), comment="参数类型")
    description = Column(Text, comment="参数说明")
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
