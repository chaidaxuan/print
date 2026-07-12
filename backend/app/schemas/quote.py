from pydantic import BaseModel, Field
from typing import List, Optional, Union
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
    spoilage: Optional[int] = Field(None, description="放数(开机损耗印张)")


class LadderPrice(BaseModel):
    """阶梯价格"""
    quantity: int = Field(..., description="数量")
    unit_price: float = Field(..., description="单价")
    total_price: float = Field(..., description="总价")


class MachineCostDetail(BaseModel):
    """单台印刷机的成本明细（用于比价展示）"""
    name: str = Field(..., description="机器名称")
    printing_size: str = Field(..., description="上机尺寸")
    plates: int = Field(..., description="版数")
    pieces_layout: str = Field(..., description="每版拼数（如 2×2=4）")
    sheets_to_print: int = Field(..., description="每版印数")
    paper_sheets: int = Field(..., description="买纸数")
    paper_cost: float = Field(..., description="纸款")
    printing_cost: float = Field(..., description="印工费")
    post_processing_cost: float = Field(..., description="后工费")
    production_cost: float = Field(..., description="生产成本")
    cost_addon: float = Field(..., description="成本附加")
    total_cost: float = Field(..., description="总成本")
    is_recommended: bool = Field(..., description="是否推荐方案")


class CalcStep(BaseModel):
    """计算轨迹单步（公式模板 + 代入真值 + 结果）"""
    key: str
    label: str = Field(..., description="步骤名，如 买纸数")
    formula: str = Field(..., description="公式模板(带中文字段名)")
    substituted: str = Field(..., description="代入真实数值")
    result: Union[float, int, str] = Field(..., description="该步结果")
    unit: Optional[str] = Field(None, description="单位")


class CutLevel(BaseModel):
    """开纸逐级对切的单级（供拼版选择过程展示）"""
    per_full: int = Field(..., description="每全张可开数 1/2/4/8…")
    level_name: str = Field(..., description="开数名：全开/对开/4开/8开")
    cut_w: float
    cut_h: float
    fits: bool = Field(..., description="能否装进机器幅面")
    selected: bool = Field(..., description="是否被选中")


class ImpositionTrace(BaseModel):
    """拼版选择轨迹"""
    press_w: float
    press_h: float
    cut_levels: List[CutLevel]
    selected_cut: str = Field(..., description="选中开纸尺寸，如 444×298")
    per_full: int
    layout_cols: int
    layout_rows: int
    pieces_per_plate: int
    layout_expr: str = Field(..., description="拼版表达，如 2×2=4")
    reason: str = Field(..., description="选中理由(自然语言)")


class PostProcItem(BaseModel):
    """后加工逐项明细"""
    name: str
    unit_price: float
    unit_label: str = Field(..., description="计价单位：元/本 等")
    qty_basis: str = Field(..., description="计费基数：本/版/页/联")
    qty: int
    raw_cost: float = Field(..., description="单价×数量(未取最低前)")
    min_charge: float = Field(..., description="最低消费")
    cost: float = Field(..., description="取 max(raw, min) 后")


class CalcTrace(BaseModel):
    """本次报价的完整计算轨迹"""
    formula_chain: List[CalcStep] = Field(..., description="逐步公式链")
    imposition: ImpositionTrace = Field(..., description="拼版选择过程")
    post_processing_items: List[PostProcItem] = Field(default=[], description="后加工逐项")


class LiandanQuoteResponse(BaseModel):
    """无碳联单报价响应"""
    quantity: int = Field(..., description="订单数量")
    unit_price: float = Field(..., description="单价")
    total_price: float = Field(..., description="总价")
    cost_breakdown: CostBreakdown = Field(..., description="成本明细")
    machine_info: MachineInfo = Field(..., description="机器信息")
    ladder_prices: List[LadderPrice] = Field(..., description="阶梯价格表")
    all_machines: List[MachineCostDetail] = Field(default=[], description="所有印刷机成本明细")
    # —— 成本明细弹窗新增（全部可选，老前端不受影响）——
    calc_trace: Optional["CalcTrace"] = Field(None, description="计算轨迹")
    post_processing_items: List["PostProcItem"] = Field(default=[], description="后加工逐项明细")
    weight_kg: Optional[float] = Field(None, description="重量(公斤)")
    volume_m3: Optional[float] = Field(None, description="体积(立方米)")
    paper_series: Optional[str] = Field(None, description="纸系列(大度/正度)")
    cut_type: Optional[str] = Field(None, description="开纸类型(如 大度8开)")
    quote_id: Optional[str] = Field(None, description="报价ID(后端记录ID)")
    quote_time: Optional[str] = Field(None, description="报价时间(ISO)")


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


class CostAddonTierResponse(BaseModel):
    """成本附加阶梯响应（单档）"""
    id: int
    category_id: int
    min_cost: float = Field(..., description="生产成本下限(含)")
    max_cost: Optional[float] = Field(None, description="生产成本上限(不含)，None 表示无上限")
    rate: float = Field(..., description="该档费率(小数，如0.10)")
    fixed_addon: float = Field(..., description="该档固定附加值(元)")
    sort_order: int = Field(..., description="排序")

    class Config:
        from_attributes = True


class CostAddonTierInput(BaseModel):
    """成本附加阶梯保存项（单档）"""
    min_cost: float = Field(..., ge=0, description="生产成本下限(含)")
    max_cost: Optional[float] = Field(None, description="生产成本上限(不含)，None 表示无上限")
    rate: float = Field(..., ge=0, description="该档费率(小数，如0.10)")
    fixed_addon: float = Field(0, ge=0, description="该档固定附加值(元)")
    sort_order: int = Field(0, description="排序")


class CostAddonTierSaveRequest(BaseModel):
    """成本附加阶梯整表保存请求"""
    category_id: int = Field(1, description="所属品类")
    tiers: List[CostAddonTierInput] = Field(..., description="阶梯档位列表，按 sort_order 顺序")


class PostProcessingParamResponse(BaseModel):
    """后工参数响应（单行）"""
    id: int
    name: str
    code: str
    group_code: Optional[str] = Field(None, description="勾选分组；单档项即 code")
    price_type: str = Field(..., description="计价单位：per_book/per_plate/per_page/per_sheet_count 等")
    unit_price: float = Field(..., description="单价")
    min_charge: float = Field(..., description="最低消费(开机费)")
    min_kai: Optional[int] = Field(None, description="开数档下限(含)，仅展示")
    max_kai: Optional[int] = Field(None, description="开数档上限(含)，选档用；None=最大档")
    sort_order: int = Field(..., description="展示排序")
    is_active: bool = Field(..., description="是否启用")

    class Config:
        from_attributes = True


class PostProcessingParamInput(BaseModel):
    """后工参数保存项（单行）"""
    name: str = Field(..., description="工序名称")
    code: str = Field(..., description="工序代码，全表唯一")
    group_code: Optional[str] = Field(None, description="勾选分组；单档项即 code")
    price_type: str = Field("per_book", description="计价单位")
    unit_price: float = Field(..., ge=0, description="单价")
    min_charge: float = Field(0, ge=0, description="最低消费(开机费)")
    min_kai: Optional[int] = Field(None, description="开数档下限(含)")
    max_kai: Optional[int] = Field(None, description="开数档上限(含)；None=最大档")
    sort_order: int = Field(0, description="展示排序")
    is_active: bool = Field(True, description="是否启用")


class PostProcessingParamSaveRequest(BaseModel):
    """后工参数整表保存请求"""
    params: List[PostProcessingParamInput] = Field(..., description="后工参数行列表")


class UnionPaperPriceResponse(BaseModel):
    """联单纸张分层价格响应"""
    id: int
    weight: int
    dadu_upper_price: float
    dadu_middle_price: float
    dadu_lower_price: float
    zhengdu_upper_price: float
    zhengdu_middle_price: float
    zhengdu_lower_price: float
    is_active: bool

    class Config:
        from_attributes = True


class UnionPaperPriceInput(BaseModel):
    """联单纸张分层价格保存项"""
    weight: int = Field(..., gt=0)
    dadu_upper_price: float = Field(0, ge=0)
    dadu_middle_price: float = Field(0, ge=0)
    dadu_lower_price: float = Field(0, ge=0)
    zhengdu_upper_price: float = Field(0, ge=0)
    zhengdu_middle_price: float = Field(0, ge=0)
    zhengdu_lower_price: float = Field(0, ge=0)
    is_active: bool = True


class UnionPaperPriceSaveRequest(BaseModel):
    """联单纸张分层价格整表保存请求"""
    papers: List[UnionPaperPriceInput]
