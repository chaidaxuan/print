from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class HuaceColorPrice(Base):
    __tablename__ = "huace_color_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    component = Column(String(20), nullable=False)
    color_code = Column(String(30), nullable=False)
    color_name = Column(String(50), nullable=False)
    price_per_version = Column(Numeric(10, 2), nullable=False, default=0)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
