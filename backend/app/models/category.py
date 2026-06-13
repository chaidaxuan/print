from sqlalchemy import Column, Integer, String, Boolean, Text, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class ProductCategory(Base):
    """产品品类模型"""

    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), nullable=False, comment="品类名称")
    code = Column(String(50), nullable=False, unique=True, comment="品类代码")
    description = Column(Text, comment="品类描述")
    icon_url = Column(String(255), comment="图标URL")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
