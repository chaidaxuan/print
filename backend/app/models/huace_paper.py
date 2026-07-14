from sqlalchemy import Column, Integer, String, Numeric, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class HuacePaperPrice(Base):
    __tablename__ = "huace_paper_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    paper_category = Column(String(50), nullable=False)
    paper_name = Column(String(50), nullable=False)
    weight = Column(Integer, nullable=False)
    ton_price = Column(Numeric(10, 2), nullable=False, default=0)
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
