from sqlalchemy import Column, Integer, DECIMAL, Boolean, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from app.database import Base


class CostAddonTier(Base):
    """成本附加阶梯模型

    依据 yinshuabaojia.com 专版联单实测反推：
      成本附加 = 生产成本 × 阶梯费率(+ 固定值)
    费率随生产成本金额递增而递减，最低档 10% 封底。
    详见 docs/LIANDAN_CALC_LOGIC.md。
    """

    __tablename__ = "cost_addon_tiers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(
        Integer,
        ForeignKey("product_categories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="所属品类",
    )
    min_cost = Column(DECIMAL(12, 2), nullable=False, comment="生产成本下限(含)")
    max_cost = Column(DECIMAL(12, 2), comment="生产成本上限(不含)，NULL 表示无上限")
    rate = Column(DECIMAL(6, 4), nullable=False, comment="该档费率(小数)")
    fixed_addon = Column(DECIMAL(10, 2), default=0, comment="该档固定附加值(元)")
    sort_order = Column(Integer, default=0, comment="排序")
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
