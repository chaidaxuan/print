from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class HuaceBinding(Base):
    __tablename__ = "huace_binding"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), nullable=False, unique=True)
    name = Column(String(50), nullable=False)
    price_type = Column(String(20), nullable=False, default="per_book")
    unit_price = Column(Numeric(10, 4), nullable=False, default=0)
    min_charge = Column(Numeric(10, 2), nullable=False, default=0)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
