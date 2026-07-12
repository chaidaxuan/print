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
    UnionPaperPrice,
    PostProcessing,
    SystemParam,
    PrintingColor,
    CostAddonTier,
)


def _layout(outer_w: float, outer_h: float, inner_w: float, inner_h: float) -> int:
    """在 outer 幅面上排布 inner 矩形，考虑旋转 90°，返回最大可拼数量。"""
    if inner_w <= 0 or inner_h <= 0:
        return 0
    a = (int(outer_w // inner_w)) * (int(outer_h // inner_h))
    b = (int(outer_w // inner_h)) * (int(outer_h // inner_w))
    return max(a, b)


def _fits(outer_w: float, outer_h: float, inner_w: float, inner_h: float) -> bool:
    """inner 矩形是否能放进 outer（考虑旋转 90°）。"""
    return (inner_w <= outer_w and inner_h <= outer_h) or (
        inner_h <= outer_w and inner_w <= outer_h
    )


def _standard_cuts(full_w: float, full_h: float, levels: int = 7):
    """由整张纸逐级对切（每次切较长边）生成标准开纸序列。

    返回 [(per_full, cut_w, cut_h), ...]，per_full 为每全张可开数：
    全开=1、对开=2、4开、8开、16开…。这是印刷行业的开纸方式，
    机器按'能装下的最大开纸'上机，而非直接把机器幅面套整张纸。
    """
    cuts = []
    w, h = full_w, full_h
    n = 1
    for _ in range(levels):
        cuts.append((n, w, h))
        if w >= h:
            w = w / 2
        else:
            h = h / 2
        n *= 2
    return cuts


# 每全张可开数 → 开数中文名，用于计算轨迹展示
LEVEL_NAMES = {
    1: "全开",
    2: "对开",
    4: "4开",
    8: "8开",
    16: "16开",
    32: "32开",
    64: "64开",
    128: "128开",
}


def _level_name(per_full: int) -> str:
    return LEVEL_NAMES.get(per_full, f"{per_full}开")


# ============ 联单分层纸款辅助函数 ============

def _get_union_layer_sequence(union_count: int) -> List[str]:
    """按联数生成纸张层序列（上/中/下）。

    2联 → [上, 下]
    3联 → [上, 中, 下]
    4联 → [上, 中, 中, 下]
    N联 → [上, (N-2)个中, 下]
    1联 → [中]  # 单联退化
    """
    if union_count <= 1:
        return ["middle"]
    elif union_count == 2:
        return ["upper", "lower"]
    else:
        return ["upper"] + ["middle"] * (union_count - 2) + ["lower"]


def _calculate_union_paper_cost(
    db: Session,
    weight: int,
    paper_type: str,
    union_count: int,
    pages_per_book: int,
    paper_sheets: int,
) -> tuple:
    """联单分层纸款计算。

    纸款 = 买纸全开张数 × 加权全开单张价。
    加权全开单张价 = 按联层比例（上/中/下页数占比）加权的 ream_price / 500。
    这与参考实现一致：纸款基于买纸数（含放数），而非有效页数。

    Args:
        weight: 克重
        paper_type: 'dadu' 或 'zhengdu'
        union_count: 联数
        pages_per_book: 每本页数
        paper_sheets: 买纸全开张数（已含放数）

    Returns:
        (总纸款, 分层明细dict)
    """
    from app.models import UnionPaperPrice

    paper_price = db.query(UnionPaperPrice).filter(UnionPaperPrice.weight == weight).first()
    if not paper_price:
        return Decimal(0), None

    prefix = "dadu" if paper_type == "dadu" else "zhengdu"
    upper_ream = Decimal(str(getattr(paper_price, f"{prefix}_upper_price", 0)))
    middle_ream = Decimal(str(getattr(paper_price, f"{prefix}_middle_price", 0)))
    lower_ream = Decimal(str(getattr(paper_price, f"{prefix}_lower_price", 0)))

    def _get_layer_ream(layer: str) -> Decimal:
        if layer == "upper":
            return upper_ream if upper_ream > 0 else (middle_ream if middle_ream > 0 else lower_ream)
        elif layer == "lower":
            return lower_ream if lower_ream > 0 else (middle_ream if middle_ream > 0 else upper_ream)
        else:
            return middle_ream if middle_ream > 0 else (upper_ream if upper_ream > 0 else lower_ream)

    LAYER_LABELS = {"upper": "上层纸", "middle": "中层纸", "lower": "下层纸"}

    layers = _get_union_layer_sequence(union_count)
    base_pages = pages_per_book // len(layers)
    remainder = pages_per_book % len(layers)

    page_distribution = []
    for i, layer in enumerate(layers):
        pages = base_pages
        if remainder > 0 and (layer == "middle" or (i == 0 and "middle" not in layers)):
            pages += remainder
            remainder = 0
        page_distribution.append((layer, pages))

    # 加权令价 = Σ(layer_pages / total_pages * layer_ream_price)
    weighted_ream = Decimal(0)
    layer_details = []
    for layer, pages in page_distribution:
        layer_ream = _get_layer_ream(layer)
        weighted_ream += layer_ream * Decimal(pages)
        layer_details.append({
            "layer": layer,
            "label": LAYER_LABELS.get(layer, layer),
            "pages": pages,
            "ream_price": float(layer_ream),
        })
    weighted_ream = weighted_ream / Decimal(pages_per_book)

    # 纸款 = 买纸全开张数 × (加权令价 / 500)
    cost = Decimal(paper_sheets) * weighted_ream / Decimal(500)
    cost = cost.quantize(Decimal("0.01"), ROUND_HALF_UP)

    paper_detail = {
        "weight": weight,
        "paper_type": paper_type,
        "paper_type_label": "大度" if paper_type == "dadu" else "正度",
        "union_count": union_count,
        "pages_per_book": pages_per_book,
        "paper_sheets": paper_sheets,
        "layers": layer_details,
        "weighted_ream_price": float(weighted_ream.quantize(Decimal("0.01"))),
        "paper_cost": float(cost),
    }

    return cost, paper_detail


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
        solutions = []
        for machine in machines:
            sol = self._solve_machine(
                machine, size_w, size_h, total_pages, color, paper,
                sheet_count=params["sheet_count"],
                pages_per_book=params["pages_per_book"],
                quantity=quantity,
            )
            if sol:
                solutions.append(sol)
        if not solutions:
            raise ValueError("无法找到合适的印刷机器")

        # 4. 后加工（对所有机器相同：版数取自颜色、开数取自成品在全开纸上的可开数，
        #    均与具体机器无关，故循环外算一次即可）
        plate_count = max(int(color.plate_count), 1)
        kai = _layout(float(paper.width or 0), float(paper.height or 0), size_w, size_h)
        post_cost, post_items = self._calculate_post_processing(
            params,
            quantity,
            plate_count=plate_count,
            total_pages=total_pages,
            sheet_count=params["sheet_count"],
            kai=kai,
        )

        # 5. 为每台机器补齐 生产成本/成本附加/总成本，供比价与明细展示
        profit_rate = params.get("profit_rate")
        category_id = params.get("category_id", 1)
        for sol in solutions:
            prod = sol["paper_cost"] + sol["printing_cost"] + post_cost
            if profit_rate is not None:
                addon = prod * Decimal(str(profit_rate))
            else:
                addon = self._calculate_cost_addon(prod, category_id)
            sol["post_processing_cost"] = post_cost
            sol["production_cost"] = prod
            sol["cost_addon"] = addon
            sol["grand_total"] = prod + addon  # 含后加工+附加的最终总成本

        # 6. 取最终总成本最低者为推荐方案
        solutions.sort(key=lambda s: s["grand_total"])
        best = solutions[0]

        production_cost = best["production_cost"]
        cost_addon = best["cost_addon"]
        total_cost = best["grand_total"]
        unit_price = total_cost / Decimal(str(quantity))

        # 成本附加率（反算，供计算轨迹展示；生产成本恒 > 0）
        addon_rate = float(cost_addon / production_cost) if production_cost else 0.0

        # 计算轨迹 + 派生展示字段（开纸类型/系列、拼版过程、逐步公式）
        paper_series = (paper.spec_name or "").replace("全开", "").strip() or "大度"
        cut_type = f"{paper_series}{_level_name(best['per_full'])}"
        calc_trace = self._build_calc_trace(
            best=best,
            quantity=quantity,
            pages_per_book=pages_per_book,
            production_cost=production_cost,
            cost_addon=cost_addon,
            total_cost=total_cost,
            unit_price=unit_price,
            addon_rate=addon_rate,
            post_cost=post_cost,
            post_items=post_items,
            paper_series=paper_series,
        )

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
                "spoilage": best["spoilage"],
            },
            "all_machines": [
                {
                    "name": s["machine_name"],
                    "printing_size": s["printing_size"],
                    "plates": s["plates"],
                    "pieces_layout": s["pieces_layout"],
                    "sheets_to_print": s["sheets_to_print"],
                    "paper_sheets": s["paper_sheets"],
                    "paper_cost": float(s["paper_cost"].quantize(Decimal("0.01"))),
                    "printing_cost": float(s["printing_cost"].quantize(Decimal("0.01"))),
                    "post_processing_cost": float(s["post_processing_cost"].quantize(Decimal("0.01"))),
                    "production_cost": float(s["production_cost"].quantize(Decimal("0.01"))),
                    "cost_addon": float(s["cost_addon"].quantize(Decimal("0.01"))),
                    "total_cost": float(s["grand_total"].quantize(Decimal("0.01"))),
                    "is_recommended": s is best,
                }
                for s in solutions
            ],
            # —— 明细弹窗新增 ——
            "calc_trace": calc_trace,
            "post_processing_items": post_items,
            "paper_series": paper_series,
            "cut_type": cut_type,
            "paper_layer_detail": best.get("paper_layer_detail"),
            "weight_kg": None,   # 按"缺失字段留空"决策暂不填
            "volume_m3": None,
        }

    # --------------------------------------------------------- 计算轨迹构建
    def _build_calc_trace(
        self,
        best: Dict,
        quantity: int,
        pages_per_book: int,
        production_cost: Decimal,
        cost_addon: Decimal,
        total_cost: Decimal,
        unit_price: Decimal,
        addon_rate: float,
        post_cost: Decimal,
        post_items: List[Dict],
        paper_series: str,
    ) -> Dict:
        """把本次报价的真实计算过程组装成结构化轨迹：
        逐步公式链（模板 + 代入真值 + 结果）、拼版逐级对切选择过程、后加工逐项。
        供成本明细弹窗如实渲染，数值全部取自 best，与实际算法一致。
        """
        tp = quantity * pages_per_book
        pcs = best["pieces_per_plate"]
        stp = best["sheets_to_print"]
        spoil = best["spoilage"]
        per_full = best["per_full"]
        psheets = best["paper_sheets"]
        per_sheet = best["per_sheet_price"]
        plates = best["plates"]
        paper_cost = best["paper_cost"]
        printing_cost = best["printing_cost"]

        def step(key, label, formula, substituted, result, unit=None):
            return {
                "key": key,
                "label": label,
                "formula": formula,
                "substituted": substituted,
                "result": result,
                "unit": unit,
            }

        post_expr = " + ".join(
            f"{i['name']}({i['cost']})" for i in post_items
        ) or "无"

        formula_chain = [
            step("total_pages", "总页数", "数量 × 每本页数",
                 f"{quantity} × {pages_per_book}", tp, "页"),
            step("sheets_to_print", "每版印数", "⌈总页数 ÷ 每版拼数⌉",
                 f"⌈{tp} ÷ {pcs}⌉", stp, "张"),
            step("paper_sheets", "买纸数", "⌈(每版印数 + 放数) ÷ 每全张可开数⌉",
                 f"⌈({stp} + {spoil}) ÷ {per_full}⌉", psheets, "全张"),
            step("paper_cost", "纸款", "全开单张纸价 × 买纸数",
                 f"{float(per_sheet):.3f} × {psheets}",
                 float(paper_cost.quantize(Decimal("0.01"))), "元"),
            step("printing_cost", "印刷费", "开机费 + 千印价×⌈印张/1000⌉ + 颜色固定增量 + 颜色印工增量×⌈印张/1000⌉",
                 f"⌈{stp}/1000⌉={-(-stp // 1000)}：(开机费 + 千印价×{-(-stp // 1000)}) + 颜色增量",
                 float(printing_cost.quantize(Decimal("0.01"))), "元"),
            step("post_processing_cost", "后加工费", "Σ 各工序 max(单价×数量, 最低消费)",
                 post_expr, float(post_cost.quantize(Decimal("0.01"))), "元"),
            step("production_cost", "生产成本", "纸款 + 印刷费 + 后加工费",
                 f"{float(paper_cost):.2f} + {float(printing_cost):.2f} + {float(post_cost):.2f}",
                 float(production_cost.quantize(Decimal("0.01"))), "元"),
            step("cost_addon", "成本附加", "生产成本 × 阶梯附加率",
                 f"{float(production_cost):.2f} × {addon_rate:.4f}",
                 float(cost_addon.quantize(Decimal("0.01"))), "元"),
            step("total_cost", "总成本", "生产成本 + 成本附加",
                 f"{float(production_cost):.2f} + {float(cost_addon):.2f}",
                 float(total_cost.quantize(Decimal("0.01"))), "元"),
            step("unit_price", "报价单价", "总成本 ÷ 数量",
                 f"{float(total_cost):.2f} ÷ {quantity}",
                 float(unit_price.quantize(Decimal("0.001"), ROUND_HALF_UP)), "元/本"),
        ]

        imposition = {
            "press_w": round(best["press_w"], 1),
            "press_h": round(best["press_h"], 1),
            "cut_levels": best["cut_levels"],
            "selected_cut": best["printing_size"],
            "per_full": per_full,
            "layout_cols": best["layout_cols"],
            "layout_rows": best["layout_rows"],
            "pieces_per_plate": pcs,
            "layout_expr": best["pieces_layout"],
            "reason": (
                f"{paper_series}{_level_name(per_full)} {best['printing_size']} 是能装进 "
                f"{best['machine_name']} 幅面 {int(best['press_w'])}×{int(best['press_h'])} "
                f"的最大标准开纸，在其上拼版 {best['pieces_layout']}"
            ),
        }

        return {
            "formula_chain": formula_chain,
            "imposition": imposition,
            "post_processing_items": post_items,
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
        sheet_count: int,
        pages_per_book: int,
        quantity: int,
    ) -> Optional[Dict]:
        """在指定机器上求解成本。

        真实印刷逻辑：机器不是直接把整张全开纸塞进去，而是先把纸开成
        能装进机器的最大标准开纸（全开/对开/4开/8开…），在该开纸上拼版。
        """
        press_w = float(machine.max_width)
        press_h = float(machine.max_height)

        full_w = float(paper.width or 0)
        full_h = float(paper.height or 0)
        if full_w <= 0 or full_h <= 0:
            return None

        # 选能装进本机的最大标准开纸（per_full 越小=开纸越大）。
        # 逐级对切全程记录，供计算轨迹展示：每级尺寸、能否上机、是否被选中。
        cut = None
        cut_levels = []
        for per_full, cut_w, cut_h in _standard_cuts(full_w, full_h):
            fits = _fits(press_w, press_h, cut_w, cut_h)
            selected = fits and cut is None  # 第一个能装进的即选中
            cut_levels.append({
                "per_full": per_full,
                "level_name": _level_name(per_full),
                "cut_w": round(cut_w, 1),
                "cut_h": round(cut_h, 1),
                "fits": fits,
                "selected": selected,
            })
            if selected:
                cut = (per_full, cut_w, cut_h)
        if cut is None:
            return None  # 最小开纸都装不进这台机器
        per_full, cut_w, cut_h = cut

        # 成品在开纸上的拼数
        pieces_per_plate = _layout(cut_w, cut_h, size_w, size_h)
        if pieces_per_plate == 0:
            return None  # 成品比开纸还大

        # 印张数
        sheets_to_print = -(-total_pages // pieces_per_plate)  # ceil

        # 放数（开机损耗，单位：印张）
        spoilage = int(self._get_system_param("default_paper_loss", 100))

        # 全开买纸数 = ceil((印张数 + 放数) / 每全张可开数)
        paper_sheets = -(-(sheets_to_print + spoilage) // per_full)  # ceil

        # 纸款：联单分层计算（按上中下纸价加权）
        # 纸系列判断：从 paper.spec_name 推断 dadu/zhengdu
        spec_name = (paper.spec_name or "").lower()
        paper_type = "dadu" if "大度" in spec_name or "dadu" in spec_name else "zhengdu"

        # 调用分层纸款逻辑（基于买纸全开张数，含放数）
        paper_cost, paper_layer_detail = _calculate_union_paper_cost(
            self.db,
            weight=int(paper.gram_weight),
            paper_type=paper_type,
            union_count=sheet_count,
            pages_per_book=pages_per_book,
            paper_sheets=paper_sheets,
        )
        # per_sheet 仅用于计算轨迹展示，分层逻辑已不依赖它，给个等效值兼容
        per_sheet = paper_cost / Decimal(paper_sheets) if paper_sheets > 0 else Decimal(0)

        # 印刷费 = 单黑基准 + 颜色固定增量 + 颜色印工增量 × k
        #   k = ⌈印张 ÷ 1000⌉（向上取整到"千印"，参考站按整千计印工，非原始除法）。
        #   单黑基准 = 开机费 + 千印价 × k（海德堡6开 60 + 20k）。
        #   颜色增量存颜色表（机器无关的颜色加价），实测反标定(27 点零误差)：
        #     单黑        fixed=0   ink=0
        #     双色/四色    fixed=70  ink=0     （四色机一遍过机，双色四色同价）
        #     N专色(1..4)  fixed=20+40N ink=10N（每专色独立一遍：开机40+印工10k）
        #     彩色+专色    fixed=180 ink=40    （=4专色，四色机4色组封顶）
        #     空白免印     fixed=0   ink=0 且基准也不收 → 由 plate_count=0 触发
        color_count = max(int(color.plate_count), 0)
        per_thousand = Decimal(str(machine.price_per_thousand))
        opening = Decimal(str(machine.opening_fee))
        k = Decimal(-(-sheets_to_print // 1000))  # ceil 到千
        fixed_fee = Decimal(str(getattr(color, "fixed_fee", 0) or 0))
        ink_extra = Decimal(str(getattr(color, "ink_per_thousand", 0) or 0))
        if color_count == 0:
            printing_cost = Decimal(0)  # 空白：不印刷，不收开机与印工
        else:
            printing_cost = (
                opening + per_thousand * k          # 单黑基准
                + fixed_fee                          # 颜色固定增量
                + ink_extra * k                      # 颜色印工增量
            )
        plates = color_count

        # 每版拼数的行列表达（如 2×2=4），仅用于展示
        cols = int(cut_w // size_w) * int(cut_h // size_h)
        rows_alt = int(cut_w // size_h) * int(cut_h // size_w)
        if rows_alt > cols:
            nx, ny = int(cut_w // size_h), int(cut_h // size_w)
        else:
            nx, ny = int(cut_w // size_w), int(cut_h // size_h)

        return {
            "machine_name": machine.name,
            "printing_size": f"{int(cut_w)}×{int(cut_h)}",
            "plates": plates,
            "pieces_per_plate": pieces_per_plate,
            "pieces_layout": f"{nx}×{ny}={pieces_per_plate}",
            "sheets_to_print": sheets_to_print,
            "spoilage": spoilage,
            "paper_sheets": paper_sheets,
            "per_full": per_full,
            "paper_cost": paper_cost,
            "printing_cost": printing_cost,
            "total_cost": paper_cost + printing_cost,
            "paper_layer_detail": paper_layer_detail,
            # —— 拼版轨迹（供计算过程展示）——
            "press_w": press_w,
            "press_h": press_h,
            "cut_levels": cut_levels,
            "layout_cols": nx,
            "layout_rows": ny,
            "per_sheet_price": per_sheet,
        }

    # ------------------------------------------------------------- 后加工费用
    # 计价单位 → 中文标签 / 计费基数标签
    _UNIT_LABEL = {
        "per_book": "元/本",
        "per_plate": "元/版",
        "per_page": "元/页",
        "per_sheet_count": "元/联",
        "per_unit": "元/个",
        "per_thousand": "元/千",
        "fixed": "元/次",
    }
    _BASIS_LABEL = {
        "per_book": "本",
        "per_plate": "版",
        "per_page": "页",
        "per_sheet_count": "联",
        "per_unit": "个",
        "per_thousand": "千",
        "fixed": "次",
    }

    def _calculate_post_processing(
        self,
        params: Dict,
        quantity: int,
        plate_count: int,
        total_pages: int,
        sheet_count: int,
        kai: int,
    ) -> tuple:
        """按前端勾选的工序分组累加后工费，返回 (总额, 逐项明细)。

        前端提交的是 group_code（如 binding/add_card/creasing）。加卡纸、装订这类
        按成品开数分多档，需用 kai 在同组内选出对应档；单档项 group_code 即 code。
        每个工序：单价×数量(视单位) 与 最低消费(min_charge) 取较大值（保底）。
        逐项明细 items 供成本明细弹窗展示每项算法（如"装订(20),加封面(30)"）。
        """
        total = Decimal("0")
        items = []
        basis_qty = {
            "per_book": quantity,
            "per_plate": plate_count,
            "per_page": total_pages,
            "per_sheet_count": sheet_count,
        }
        for group in params.get("post_processing", []):
            proc = self._resolve_processing(group, kai)
            if not proc:
                continue
            raw = self._unit_cost(
                proc, quantity, plate_count, total_pages, sheet_count
            )
            min_charge = Decimal(str(proc.min_charge or 0))
            cost = max(raw, min_charge)
            unit = proc.price_type.value if proc.price_type else "per_book"
            items.append({
                "name": proc.name,
                "unit_price": float(Decimal(str(proc.unit_price))),
                "unit_label": self._UNIT_LABEL.get(unit, "元/本"),
                "qty_basis": self._BASIS_LABEL.get(unit, "本"),
                "qty": int(basis_qty.get(unit, quantity)),
                "raw_cost": float(raw.quantize(Decimal("0.01"), ROUND_HALF_UP)),
                "min_charge": float(min_charge),
                "cost": float(cost.quantize(Decimal("0.01"), ROUND_HALF_UP)),
            })
            total += cost
        return total, items

    def _resolve_processing(self, group_code: str, kai: int) -> Optional[PostProcessing]:
        """在同一 group_code 下按成品开数(kai)选出对应档位。

        选档规则：升序按 max_kai 取第一个 max_kai >= kai 的档，自动闭合相邻档间的
        缝隙（如 19 开介于 11-18 与 20-50 之间仍归入 20-50 档）；max_kai 为 NULL
        表示无上限档（如"50开以上"），作为兜底。单档项(如加封面)只有一行直接返回。
        """
        rows = (
            self.db.query(PostProcessing)
            .filter(
                PostProcessing.group_code == group_code,
                PostProcessing.is_active == True,  # noqa: E712
            )
            .all()
        )
        if not rows:
            return None
        banded = [r for r in rows if r.max_kai is not None]
        unbounded = [r for r in rows if r.max_kai is None]
        for r in sorted(banded, key=lambda x: x.max_kai):
            if kai <= r.max_kai:
                return r
        if unbounded:
            return unbounded[0]
        return banded[-1] if banded else None

    def _unit_cost(
        self,
        proc: PostProcessing,
        quantity: int,
        plate_count: int,
        total_pages: int,
        sheet_count: int,
    ) -> Decimal:
        """按计价单位算未取最低消费前的费用。"""
        unit = proc.price_type.value if proc.price_type else "per_book"
        up = Decimal(str(proc.unit_price))
        if unit == "per_book":
            return up * Decimal(quantity)
        if unit == "per_plate":
            return up * Decimal(plate_count)
        if unit == "per_page":
            return up * Decimal(total_pages)
        if unit == "per_sheet_count":
            return up * Decimal(sheet_count)
        # 旧值兼容
        if unit == "per_thousand":
            return up * Decimal(quantity) / Decimal(1000)
        if unit == "fixed":
            return up
        return up * Decimal(quantity)  # per_unit 兜底

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

    # ----------------------------------------------------------- 成本附加(阶梯)
    def _calculate_cost_addon(self, production_cost: Decimal, category_id: int) -> Decimal:
        """按生产成本金额查阶梯表，返回成本附加 = 生产成本 × 费率 + 固定值。

        实测(yinshuabaojia.com 专版联单)：费率随生产成本递增而递减，最低 10% 封底。
        若表中无匹配档位（如未初始化），回退到旧的固定系数 cost_markup_rate。
        详见 docs/LIANDAN_CALC_LOGIC.md。
        """
        tier = (
            self.db.query(CostAddonTier)
            .filter(
                CostAddonTier.category_id == category_id,
                CostAddonTier.is_active == True,  # noqa: E712
                CostAddonTier.min_cost <= production_cost,
                (CostAddonTier.max_cost == None)  # noqa: E711
                | (CostAddonTier.max_cost > production_cost),
            )
            .order_by(CostAddonTier.sort_order)
            .first()
        )
        if tier is None:
            # 回退：阶梯表未配置时用旧系数，保证不崩
            markup = Decimal(str(self._get_system_param("cost_markup_rate", 0.609)))
            return production_cost * markup
        rate = Decimal(str(tier.rate))
        fixed = Decimal(str(tier.fixed_addon or 0))
        return production_cost * rate + fixed

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
