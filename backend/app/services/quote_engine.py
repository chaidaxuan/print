"""
无碳联单报价计算引擎
基于 yinshuabaojia.com 观察到的业务逻辑实现（原创代码）

计算链路（自顶向下）：
  成品尺寸 → 在「上机开纸」(机器幅面，如大度8开 420×285) 上拼版 → 每版拼数
  总页数 = 订单数量 × 每本页数
  印张数 = ceil(总页数 / 每版拼数)
  全开买纸数 = ceil((印张数 + 放数) / 每全张可开数)
  纸款 = 全开买纸数 × 全开单张纸价
  印刷费 = 版数 × (开机费 + 印张数/1000 × 千印价)
  后加工费 = Σ 工序单价 × 数量
  生产成本 = 纸款 + 印刷费 + 后加工费
  成本附加 = 生产成本 × 成本附加率
  总成本 = 生产成本 + 成本附加
  报价单价 = 总成本 / 数量
系统比较多台印刷机，选总成本最低的方案作为推荐。
"""
from typing import Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP
from sqlalchemy.orm import Session
from app.models import (
    ProductSize,
    PrintingMachine,
    PaperSpec,
    PostProcessing,
    SystemParam,
    PrintingColor,
)


def _layout(outer_w: float, outer_h: float, inner_w: float, inner_h: float) -> int:
    """在 outer 幅面上排布 inner 矩形，考虑旋转 90°，返回最大可拼数量。"""
    if inner_w <= 0 or inner_h <= 0:
        return 0
    a = (int(outer_w // inner_w)) * (int(outer_h // inner_h))
    b = (int(outer_w // inner_h)) * (int(outer_h // inner_w))
    return max(a, b)


class LiandanQuoteEngine:
    """无碳联单报价计算引擎"""

    LADDER_QUANTITIES = [100, 200, 300, 400, 500]

    def __init__(self, db: Session):
        self.db = db

    # ----------------------------------------------------------------- 对外入口
    def calculate(self, params: Dict) -> Dict:
        """计算报价（含成本明细、推荐机器、阶梯价格表）。"""
        result = self._calculate_single(params)
        result["ladder_prices"] = self._calculate_ladder_prices(
            params, self.LADDER_QUANTITIES
        )
        return result

    # --------------------------------------------------------------- 单数量计算
    def _calculate_single(self, params: Dict) -> Dict:
        """计算单一数量的报价（不含阶梯表，供主流程与阶梯循环复用）。"""

        # 1. 基础数据
        size = (
            self.db.query(ProductSize)
            .filter(ProductSize.id == params["size_id"])
            .first()
        )
        if not size:
            raise ValueError("成品尺寸不存在")

        # 支持自定义尺寸
        size_w = float(params.get("custom_width") or size.width)
        size_h = float(params.get("custom_height") or size.height)

        color = (
            self.db.query(PrintingColor)
            .filter(PrintingColor.code == params["color_code"])
            .first()
        )
        if not color:
            raise ValueError("印刷颜色不存在")

        quantity = params["quantity"]
        pages_per_book = params["pages_per_book"]
        total_pages = quantity * pages_per_book

        # 2. 选纸（按克重）
        paper = (
            self.db.query(PaperSpec)
            .filter(
                PaperSpec.gram_weight == params["gram_weight"],
                PaperSpec.is_active == True,  # noqa: E712
            )
            .first()
        )
        if not paper:
            raise ValueError("无匹配的纸张规格")

        # 3. 多机器比价，取最优
        machines = (
            self.db.query(PrintingMachine)
            .filter(PrintingMachine.is_active == True)  # noqa: E712
            .all()
        )
        best = None
        for machine in machines:
            sol = self._solve_machine(
                machine, size_w, size_h, total_pages, color, paper
            )
            if sol and (best is None or sol["total_cost"] < best["total_cost"]):
                best = sol
        if not best:
            raise ValueError("无法找到合适的印刷机器")

        # 4. 后加工
        post_cost = self._calculate_post_processing(params, quantity)

        # 5. 汇总
        production_cost = best["paper_cost"] + best["printing_cost"] + post_cost

        # 利润率：自填优先，否则取系统成本附加率
        if params.get("profit_rate") is not None:
            markup = Decimal(str(params["profit_rate"]))
        else:
            markup = Decimal(str(self._get_system_param("cost_markup_rate", 0.609)))
        cost_addon = production_cost * markup

        total_cost = production_cost + cost_addon
        unit_price = total_cost / Decimal(str(quantity))

        return {
            "quantity": quantity,
            "unit_price": float(unit_price.quantize(Decimal("0.001"), ROUND_HALF_UP)),
            "total_price": float(total_cost.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            "cost_breakdown": {
                "paper_cost": float(best["paper_cost"].quantize(Decimal("0.01"))),
                "printing_cost": float(best["printing_cost"].quantize(Decimal("0.01"))),
                "post_processing_cost": float(post_cost.quantize(Decimal("0.01"))),
                "production_cost": float(production_cost.quantize(Decimal("0.01"))),
                "cost_addon": float(cost_addon.quantize(Decimal("0.01"))),
                "total_cost": float(total_cost.quantize(Decimal("0.01"))),
            },
            "machine_info": {
                "name": best["machine_name"],
                "printing_size": best["printing_size"],
                "plates": best["plates"],
                "pieces_per_plate": best["pieces_per_plate"],
                "sheets_to_print": best["sheets_to_print"],
                "paper_sheets": best["paper_sheets"],
            },
        }

    # ----------------------------------------------------------- 单台机器求解
    def _solve_machine(
        self,
        machine: PrintingMachine,
        size_w: float,
        size_h: float,
        total_pages: int,
        color: PrintingColor,
        paper: PaperSpec,
    ) -> Optional[Dict]:
        """在指定机器的上机幅面上求解成本。"""
        press_w = float(machine.max_width)
        press_h = float(machine.max_height)

        # 成品在上机幅面上的拼数
        pieces_per_plate = _layout(press_w, press_h, size_w, size_h)
        if pieces_per_plate == 0:
            return None  # 成品比幅面还大，机器不适用

        # 上机幅面能从一张全开纸上裁出几张（每全张可开数）
        full_w = float(paper.width or 0)
        full_h = float(paper.height or 0)
        per_full = _layout(full_w, full_h, press_w, press_h)
        if per_full == 0:
            return None  # 上机幅面比全开纸还大，该纸不适用

        # 印张数
        sheets_to_print = -(-total_pages // pieces_per_plate)  # ceil

        # 放数（开机损耗，单位：印张）
        spoilage = int(self._get_system_param("default_paper_loss", 100))

        # 全开买纸数
        paper_sheets = -(-(sheets_to_print + spoilage) // per_full)  # ceil
        paper_cost = Decimal(str(paper.price_per_sheet)) * paper_sheets

        # 印刷费：版数 × (开机费 + 印张/1000 × 千印价)
        plates = max(int(color.plate_count), 1)
        per_thousand = Decimal(str(machine.price_per_thousand))
        opening = Decimal(str(machine.opening_fee))
        printing_cost = plates * (
            opening + (per_thousand * Decimal(sheets_to_print) / Decimal(1000))
        )

        return {
            "machine_name": machine.name,
            "printing_size": f"{int(press_w)}×{int(press_h)}",
            "plates": plates,
            "pieces_per_plate": pieces_per_plate,
            "sheets_to_print": sheets_to_print,
            "paper_sheets": paper_sheets,
            "paper_cost": paper_cost,
            "printing_cost": printing_cost,
            "total_cost": paper_cost + printing_cost,
        }

    # ------------------------------------------------------------- 后加工费用
    def _calculate_post_processing(self, params: Dict, quantity: int) -> Decimal:
        total = Decimal("0")
        for code in params.get("post_processing", []):
            proc = (
                self.db.query(PostProcessing)
                .filter(
                    PostProcessing.code == code,
                    PostProcessing.is_active == True,  # noqa: E712
                )
                .first()
            )
            if not proc:
                continue
            if proc.price_type and proc.price_type.value == "fixed":
                cost = Decimal(str(proc.unit_price))
            elif proc.price_type and proc.price_type.value == "per_thousand":
                cost = Decimal(str(proc.unit_price)) * Decimal(quantity) / Decimal(1000)
            else:  # per_unit
                cost = Decimal(str(proc.unit_price)) * Decimal(quantity)
            min_charge = Decimal(str(proc.min_charge or 0))
            if cost < min_charge:
                cost = min_charge
            total += cost
        return total

    # --------------------------------------------------------------- 系统参数
    def _get_system_param(self, key: str, default) -> float:
        param = (
            self.db.query(SystemParam)
            .filter(SystemParam.param_key == key)
            .first()
        )
        if param:
            try:
                return float(param.param_value)
            except (TypeError, ValueError):
                return default
        return default

    # --------------------------------------------------------------- 阶梯价格
    def _calculate_ladder_prices(
        self, params: Dict, quantities: List[int]
    ) -> List[Dict]:
        results = []
        original_qty = params["quantity"]
        for qty in quantities:
            params["quantity"] = qty
            single = self._calculate_single(params)
            results.append(
                {
                    "quantity": qty,
                    "unit_price": single["unit_price"],
                    "total_price": single["total_price"],
                }
            )
        params["quantity"] = original_qty
        return results
