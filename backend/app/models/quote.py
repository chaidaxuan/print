from sqlalchemy import Column, Integer, String, DECIMAL, JSON, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class QuoteRecord(Base):
    """报价记录模型"""

    __tablename__ = "quote_records"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("product_categories.id"), nullable=False, index=True)
    quote_no = Column(String(50), unique=True, comment="报价单号")
    customer_name = Column(String(100), comment="客户名称")
    product_name = Column(String(200), comment="产品名称")

    # 表单数据和计算结果
    form_data = Column(JSON, comment="表单参数")
    cost_breakdown = Column(JSON, comment="成本明细")
    unit_price = Column(DECIMAL(10, 4), comment="单价")
    total_price = Column(DECIMAL(10, 2), comment="总价")
    quantity = Column(Integer, comment="数量")

    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
