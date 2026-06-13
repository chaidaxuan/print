from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, ForeignKey
from app.database import Base


class ProductSize(Base):
    """成品尺寸规格模型"""

    __tablename__ = "product_sizes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey("product_categories.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(50), nullable=False, comment="尺寸名称")
    width = Column(DECIMAL(10, 2), nullable=False, comment="宽度(mm)")
    height = Column(DECIMAL(10, 2), nullable=False, comment="高度(mm)")
    code = Column(String(50), comment="尺寸代码")
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
