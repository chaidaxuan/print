from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class HuaceClientTier(Base):
    __tablename__ = "huace_client_tiers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    multiplier = Column(Numeric(6, 4), nullable=False, default=1)
    remark = Column(String(200))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
