from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal


# ============ 请求 ============

class HuaceQuoteRequest(BaseModel):
    """画册报价请求"""
    size_id: int = Field(..., description="成品尺寸ID")
    quantity: int = Field(..., gt=0, description="订单数量（本）")
    cover_paper_name: str = Field(..., description="封面纸名")
    cover_paper_weight: int = Field(..., description="封面纸克重")
    cover_paper_ton_price: float = Field(..., description="封面纸吨价")
    cover_pages: int = Field(4, ge=4, description="封面P数(通常4)")
    cover_color_code: str = Field(..., description="封面印刷颜色代码")
    cover_both_sides: bool = Field(True, description="封面双面印(自反版)")
    inner_paper_name: str = Field(..., description="内页纸名")
    inner_paper_weight: int = Field(..., description="内页纸克重")
    inner_paper_ton_price: float = Field(..., description="内页纸吨价")
    inner_pages: int = Field(..., ge=4, description="内页P数")
    inner_color_code: str = Field(..., description="内页印刷颜色代码")
    binding_code: str = Field(..., description="装订方式代码")
    surface_treatment: Optional[str] = Field(None, description="表面处理工序代码(单选)")
    other_processing: List[str] = Field(default=[], description="其他后道工序代码列表")
    client_tier_code: str = Field("cost", description="客户类型代码")
    multi_quantities: List[int] = Field(default=[], description="多数量(阶梯报价)")
    customer_name: Optional[str] = Field(None, description="客户名称")
    product_name: Optional[str] = Field(None, description="产品名称")


# ============ 响应子模型 ============

class HuaceCostBreakdown(BaseModel):
    """画册成本明细"""
    paper_cost: float = Field(..., description="纸款合计")
    printing_cost: float = Field(..., description="印刷费合计")
    surface_cost: float = Field(..., description="表面处理费")
    binding_cost: float = Field(..., description="装订费")
    other_post_cost: float = Field(..., description="其他后道费")
    total_cost: float = Field(..., description="成本总计")


class HuaceTierPrice(BaseModel):
    """客户类型价格"""
    code: str
    name: str
    multiplier: float
    total_price: float
    unit_price: float


class HuaceLadderPrice(BaseModel):
    """阶梯数量报价"""
    quantity: int
    cost_breakdown: HuaceCostBreakdown
    tier_prices: List[HuaceTierPrice]


class HuaceCalcStep(BaseModel):
    """计算轨迹单步"""
    key: str
    label: str
    formula: str
    substituted: str
    result: float | int | str
    unit: Optional[str] = None


class HuaceQuoteResponse(BaseModel):
    """画册报价响应"""
    quantity: int
    cost_breakdown: HuaceCostBreakdown
    tier_prices: List[HuaceTierPrice]
    ladder_prices: List[HuaceLadderPrice]
    calc_trace: List[HuaceCalcStep] = []
    quote_id: Optional[str] = None
    quote_time: Optional[str] = None


# ============ 下拉数据响应 ============

class HuaceSizeResponse(BaseModel):
    id: int
    name: str
    width: float
    height: float
    code: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True


class HuacePaperResponse(BaseModel):
    id: int
    paper_category: str
    paper_name: str
    weight: int
    ton_price: float
    sort_order: int

    class Config:
        from_attributes = True


class HuaceColorResponse(BaseModel):
    id: int
    component: str
    color_code: str
    color_name: str
    price_per_version: float
    sort_order: int

    class Config:
        from_attributes = True


class HuaceBindingResponse(BaseModel):
    id: int
    code: str
    name: str
    price_type: str
    unit_price: float
    min_charge: float
    sort_order: int

    class Config:
        from_attributes = True


class HuacePostProcessingResponse(BaseModel):
    id: int
    code: str
    name: str
    proc_group: str
    price_type: str
    unit_price: float
    min_charge: float
    sort_order: int

    class Config:
        from_attributes = True


class HuaceClientTierResponse(BaseModel):
    id: int
    code: str
    name: str
    multiplier: float
    remark: Optional[str] = None
    sort_order: int

    class Config:
        from_attributes = True
