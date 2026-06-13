from pydantic import BaseModel, Field
from typing import List, Optional
from decimal import Decimal


class LiandanQuoteRequest(BaseModel):
    """无碳联单报价请求"""
    size_id: int = Field(..., description="成品尺寸ID")
    quantity: int = Field(..., gt=0, description="订单数量（本）")
    sheet_count: int = Field(..., ge=2, le=6, description="联数（2-6联）")
    pages_per_book: int = Field(..., gt=0, description="每本页数")
    color_code: str = Field(..., description="印刷颜色代码")
    gram_weight: int = Field(..., description="纸张克重")
    post_processing: List[str] = Field(default=[], description="后道工序代码列表")
    custom_width: Optional[float] = Field(None, description="自定义成品宽度(mm)")
    custom_height: Optional[float] = Field(None, description="自定义成品高度(mm)")
    profit_rate: Optional[float] = Field(None, description="自填利润率(小数，如0.6)")
    customer_name: Optional[str] = Field(None, description="客户名称")
    product_name: Optional[str] = Field(None, description="产品名称")


class CostBreakdown(BaseModel):
    """成本明细"""
    paper_cost: float = Field(..., description="纸款")
    printing_cost: float = Field(..., description="印刷费")
    post_processing_cost: float = Field(..., description="后加工费")
    production_cost: float = Field(..., description="生产成本")
    cost_addon: float = Field(..., description="成本附加")
    total_cost: float = Field(..., description="总成本")


class MachineInfo(BaseModel):
    """机器信息"""
    name: str = Field(..., description="机器名称")
    printing_size: str = Field(..., description="印刷尺寸")
    plates: int = Field(..., description="版数")
    pieces_per_plate: int = Field(..., description="每版拼数")
    sheets_to_print: int = Field(..., description="印张数")
    paper_sheets: int = Field(..., description="买纸数")


class LadderPrice(BaseModel):
    """阶梯价格"""
    quantity: int = Field(..., description="数量")
    unit_price: float = Field(..., description="单价")
    total_price: float = Field(..., description="总价")


class LiandanQuoteResponse(BaseModel):
    """无碳联单报价响应"""
    quantity: int = Field(..., description="订单数量")
    unit_price: float = Field(..., description="单价")
    total_price: float = Field(..., description="总价")
    cost_breakdown: CostBreakdown = Field(..., description="成本明细")
    machine_info: MachineInfo = Field(..., description="机器信息")
    ladder_prices: List[LadderPrice] = Field(..., description="阶梯价格表")


class ProductSizeResponse(BaseModel):
    """成品尺寸响应"""
    id: int
    name: str
    width: float
    height: float
    code: Optional[str] = None

    class Config:
        from_attributes = True


class PrintingColorResponse(BaseModel):
    """印刷颜色响应"""
    id: int
    name: str
    code: str
    plate_count: int

    class Config:
        from_attributes = True


class PostProcessingResponse(BaseModel):
    """后道工序响应"""
    id: int
    name: str
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True
