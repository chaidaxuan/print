"""
专版画册报价计算引擎

计算链路：
  纸款 = 封面纸款 + 内页纸款
    每张全开成本 = 全开面积(m²) × 克重/1000 × 吨价/1000
    press张 = ⌈qty / books_per_full⌉
    买纸数 = press张 + 放数
    纸款 = 买纸数 × 每张全开成本
  印刷费 = 封面版数×封面色价 + 内页版数×内页色价
  表面处理 = max(封面买纸数 × 全开面积 × 单价, 最低消费)
  装订费 = max(qty × 单价, 最低消费)
  其他后道 = Σ max(qty × 单价, 最低消费)
  成本价 = 纸款 + 印刷费 + 表面处理 + 装订费 + 其他后道
  客户报价 = 成本价 × 客户倍率
"""
import math
from decimal import Decimal, ROUND_HALF_UP, ROUND_CEILING
from typing import Dict, List, Any
from sqlalchemy.orm import Session

from app.models.huace_color import HuaceColorPrice
from app.models.huace_binding import HuaceBinding
from app.models.huace_post_processing import HuacePostProcessing
from app.models.huace_client_tier import HuaceClientTier
from app.models import ProductSize

DADU_FULL_W = 889
DADU_FULL_H = 1194
ZHENGDU_FULL_W = 787
ZHENGDU_FULL_H = 1092

DADU_FULL_AREA = Decimal(str(DADU_FULL_W)) * Decimal(str(DADU_FULL_H)) / Decimal("1000000")
ZHENGDU_FULL_AREA = Decimal(str(ZHENGDU_FULL_W)) * Decimal(str(ZHENGDU_FULL_H)) / Decimal("1000000")


def _spoilage(versions: int, press_sheets: int) -> int:
    """放数公式（逆向拟合）"""
    return round(19 + 8.47 * versions + press_sheets * 0.00422)


class HuaceQuoteEngine:
    def __init__(self, db: Session):
        self.db = db

    def calculate(self, params: Dict) -> Dict:
        size = self.db.query(ProductSize).filter(ProductSize.id == params["size_id"]).first()
        if not size:
            raise ValueError("无效的成品尺寸")

        is_dadu = size.code.startswith("dadu") if size.code else True
        full_w = DADU_FULL_W if is_dadu else ZHENGDU_FULL_W
        full_h = DADU_FULL_H if is_dadu else ZHENGDU_FULL_H
        full_area = DADU_FULL_AREA if is_dadu else ZHENGDU_FULL_AREA

        kai = self._get_kai(size)
        qty = params["quantity"]
        cover_pages = params.get("cover_pages", 4)
        inner_pages = params["inner_pages"]

        cover_weight = params["cover_paper_weight"]
        cover_ton_price = params["cover_paper_ton_price"]
        inner_weight = params["inner_paper_weight"]
        inner_ton_price = params["inner_paper_ton_price"]

        cover_color = self.db.query(HuaceColorPrice).filter(
            HuaceColorPrice.component == "cover",
            HuaceColorPrice.color_code == params["cover_color_code"],
            HuaceColorPrice.is_active == True
        ).first()
        inner_color = self.db.query(HuaceColorPrice).filter(
            HuaceColorPrice.component == "inner",
            HuaceColorPrice.color_code == params["inner_color_code"],
            HuaceColorPrice.is_active == True
        ).first()
        if not cover_color or not inner_color:
            raise ValueError("无效的印刷颜色")

        trace: List[Dict] = []

        # === 封面纸款 ===
        cover_sheet_cost = full_area * Decimal(str(cover_weight)) / Decimal("1000") * Decimal(str(cover_ton_price)) / Decimal("1000")
        cover_books_per_full = kai * 2 // cover_pages
        cover_press = math.ceil(qty / cover_books_per_full)
        cover_versions = 1
        cover_spoilage = _spoilage(cover_versions, cover_press)
        cover_buy = cover_press + cover_spoilage
        cover_paper_cost = (Decimal(str(cover_buy)) * cover_sheet_cost).quantize(Decimal("1"), ROUND_CEILING)

        trace.append({"key": "cover_sheet_cost", "label": "封面每张全开成本",
                      "formula": "全开面积(m²) × 克重/1000 × 吨价/1000",
                      "substituted": f"{float(full_area):.4f} × {cover_weight}/1000 × {cover_ton_price}/1000",
                      "result": float(cover_sheet_cost.quantize(Decimal("0.001"))), "unit": "元/张"})
        trace.append({"key": "cover_books_per_full", "label": "封面每全开本数",
                      "formula": "开数×2 ÷ 封面P数",
                      "substituted": f"{kai}×2 ÷ {cover_pages}",
                      "result": cover_books_per_full, "unit": "本/全开"})
        trace.append({"key": "cover_press", "label": "封面印张数",
                      "formula": "⌈数量 ÷ 每全开本数⌉",
                      "substituted": f"⌈{qty} ÷ {cover_books_per_full}⌉",
                      "result": cover_press, "unit": "张"})
        trace.append({"key": "cover_spoilage", "label": "封面放数",
                      "formula": "round(19 + 8.47×版数 + press×0.00422)",
                      "substituted": f"round(19 + 8.47×{cover_versions} + {cover_press}×0.00422)",
                      "result": cover_spoilage, "unit": "张"})
        trace.append({"key": "cover_buy", "label": "封面买纸数",
                      "formula": "印张数 + 放数",
                      "substituted": f"{cover_press} + {cover_spoilage}",
                      "result": cover_buy, "unit": "张"})
        trace.append({"key": "cover_paper_cost", "label": "封面纸款",
                      "formula": "买纸数 × 每张全开成本",
                      "substituted": f"{cover_buy} × {float(cover_sheet_cost):.4f}",
                      "result": float(cover_paper_cost.quantize(Decimal("1"), ROUND_HALF_UP)), "unit": "元"})

        # === 内页纸款 ===
        inner_sheet_cost = full_area * Decimal(str(inner_weight)) / Decimal("1000") * Decimal(str(inner_ton_price)) / Decimal("1000")
        inner_books_per_full = kai * 2 // inner_pages
        if inner_books_per_full < 1:
            inner_books_per_full = 1
        inner_press = math.ceil(qty / inner_books_per_full)
        # 内页版数 = P数×4÷开数 (memory: P16, kai16 → 4版)
        inner_versions = inner_pages * 4 // kai

        inner_spoilage = _spoilage(inner_versions, inner_press)
        inner_buy = inner_press + inner_spoilage
        inner_paper_cost = (Decimal(str(inner_buy)) * inner_sheet_cost).quantize(Decimal("1"), ROUND_CEILING)

        trace.append({"key": "inner_sheet_cost", "label": "内页每张全开成本",
                      "formula": "全开面积(m²) × 克重/1000 × 吨价/1000",
                      "substituted": f"{float(full_area):.4f} × {inner_weight}/1000 × {inner_ton_price}/1000",
                      "result": float(inner_sheet_cost.quantize(Decimal("0.001"))), "unit": "元/张"})
        trace.append({"key": "inner_versions", "label": "内页版数",
                      "formula": "内页P数 × 4 ÷ 开数",
                      "substituted": f"{inner_pages} × 4 ÷ {kai}",
                      "result": inner_versions, "unit": "版"})
        trace.append({"key": "inner_books_per_full", "label": "内页每全开本数",
                      "formula": "开数×2 ÷ 内页P数",
                      "substituted": f"{kai}×2 ÷ {inner_pages}",
                      "result": inner_books_per_full, "unit": "本/全开"})
        trace.append({"key": "inner_press", "label": "内页印张数",
                      "formula": "⌈数量 ÷ 每全开本数⌉",
                      "substituted": f"⌈{qty} ÷ {inner_books_per_full}⌉",
                      "result": inner_press, "unit": "张"})
        trace.append({"key": "inner_spoilage", "label": "内页放数",
                      "formula": "round(19 + 8.47×版数 + press×0.00422)",
                      "substituted": f"round(19 + 8.47×{inner_versions} + {inner_press}×0.00422)",
                      "result": inner_spoilage, "unit": "张"})
        trace.append({"key": "inner_buy", "label": "内页买纸数",
                      "formula": "印张数 + 放数",
                      "substituted": f"{inner_press} + {inner_spoilage}",
                      "result": inner_buy, "unit": "张"})
        trace.append({"key": "inner_paper_cost", "label": "内页纸款",
                      "formula": "买纸数 × 每张全开成本",
                      "substituted": f"{inner_buy} × {float(inner_sheet_cost):.4f}",
                      "result": float(inner_paper_cost.quantize(Decimal("1"), ROUND_HALF_UP)), "unit": "元"})

        paper_cost = cover_paper_cost + inner_paper_cost

        # === 印刷费 ===
        cover_printing_cost = Decimal(str(cover_versions)) * Decimal(str(cover_color.price_per_version))
        inner_printing_cost = Decimal(str(inner_versions)) * Decimal(str(inner_color.price_per_version))
        printing_cost = cover_printing_cost + inner_printing_cost

        trace.append({"key": "cover_printing", "label": "封面印刷费",
                      "formula": "封面版数 × 封面色价",
                      "substituted": f"{cover_versions} × {cover_color.price_per_version}",
                      "result": float(cover_printing_cost), "unit": "元"})
        trace.append({"key": "inner_printing", "label": "内页印刷费",
                      "formula": "内页版数 × 内页色价",
                      "substituted": f"{inner_versions} × {inner_color.price_per_version}",
                      "result": float(inner_printing_cost), "unit": "元"})

        # === 表面处理（封面） ===
        surface_cost = Decimal("0")
        surface_code = params.get("surface_treatment")
        surface_codes = [surface_code] if surface_code else []
        for code in surface_codes:
            proc = self.db.query(HuacePostProcessing).filter(
                HuacePostProcessing.code == code,
                HuacePostProcessing.proc_group == "surface",
                HuacePostProcessing.is_active == True
            ).first()
            if proc:
                raw = Decimal(str(cover_buy)) * full_area * Decimal(str(proc.unit_price))
                cost = max(raw, Decimal(str(proc.min_charge)))
                surface_cost += cost

        trace.append({"key": "surface_cost", "label": "表面处理费",
                      "formula": "max(封面买纸数 × 全开面积 × 单价, 最低消费)",
                      "substituted": f"封面买纸{cover_buy}张, 面积{float(full_area):.4f}m², 工序{len(surface_codes)}项",
                      "result": float(surface_cost.quantize(Decimal("1"), ROUND_HALF_UP)), "unit": "元"})

        # === 装订费 ===
        binding_code = params.get("binding_code", "saddle_stitch")
        binding = self.db.query(HuaceBinding).filter(
            HuaceBinding.code == binding_code,
            HuaceBinding.is_active == True
        ).first()
        binding_cost = Decimal("0")
        if binding:
            raw = Decimal(str(qty)) * Decimal(str(binding.unit_price))
            binding_cost = max(raw, Decimal(str(binding.min_charge)))

        trace.append({"key": "binding_cost", "label": "装订费",
                      "formula": "max(数量 × 单价, 最低消费)",
                      "substituted": f"max({qty} × {binding.unit_price if binding else 0}, {binding.min_charge if binding else 0})",
                      "result": float(binding_cost.quantize(Decimal("1"), ROUND_HALF_UP)), "unit": "元"})

        # === 其他后道 ===
        other_cost = Decimal("0")
        other_codes = params.get("other_processing", [])
        for code in other_codes:
            proc = self.db.query(HuacePostProcessing).filter(
                HuacePostProcessing.code == code,
                HuacePostProcessing.proc_group == "other",
                HuacePostProcessing.is_active == True
            ).first()
            if proc:
                if proc.price_type == "per_book":
                    raw = Decimal(str(qty)) * Decimal(str(proc.unit_price))
                else:
                    raw = Decimal(str(proc.min_charge))
                cost = max(raw, Decimal(str(proc.min_charge)))
                other_cost += cost

        # === 成本汇总 ===
        total_cost = paper_cost + printing_cost + surface_cost + binding_cost + other_cost
        total_cost_rounded = float(total_cost.quantize(Decimal("1"), ROUND_HALF_UP))

        trace.append({"key": "total_cost", "label": "成本合计",
                      "formula": "纸款 + 印刷费 + 表面处理 + 装订费 + 其他后道",
                      "substituted": f"{float(paper_cost.quantize(Decimal('1'), ROUND_HALF_UP))} + {float(printing_cost)} + {float(surface_cost.quantize(Decimal('1'), ROUND_HALF_UP))} + {float(binding_cost.quantize(Decimal('1'), ROUND_HALF_UP))} + {float(other_cost.quantize(Decimal('1'), ROUND_HALF_UP))}",
                      "result": total_cost_rounded, "unit": "元"})

        # === 客户倍率 ===
        tiers = self.db.query(HuaceClientTier).filter(
            HuaceClientTier.is_active == True
        ).order_by(HuaceClientTier.sort_order).all()

        tier_prices = []
        for t in tiers:
            tp = float((total_cost * Decimal(str(t.multiplier))).quantize(Decimal("0.01"), ROUND_HALF_UP))
            up = round(tp / qty, 4) if qty > 0 else 0
            tier_prices.append({
                "code": t.code,
                "name": t.name,
                "multiplier": float(t.multiplier),
                "total_price": tp,
                "unit_price": up,
            })

        # === 阶梯报价 ===
        multi_quantities = params.get("multi_quantities", [])
        all_quantities = [qty] + [q for q in multi_quantities if q != qty and q > 0]
        ladder_prices = []
        for q in all_quantities:
            lp = self._calc_for_qty(q, kai, full_area,
                                    cover_weight, cover_ton_price,
                                    inner_weight, inner_ton_price,
                                    cover_pages, inner_pages,
                                    cover_versions, inner_versions,
                                    cover_color, inner_color,
                                    surface_codes, binding, other_codes, tiers)
            ladder_prices.append(lp)

        cost_breakdown = {
            "paper_cost": float(paper_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "printing_cost": float(printing_cost),
            "surface_cost": float(surface_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "binding_cost": float(binding_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "other_post_cost": float(other_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "total_cost": total_cost_rounded,
        }

        return {
            "quantity": qty,
            "cost_breakdown": cost_breakdown,
            "tier_prices": tier_prices,
            "ladder_prices": ladder_prices,
            "calc_trace": trace,
        }

    def _calc_for_qty(self, qty, kai, full_area,
                      cover_weight, cover_ton_price,
                      inner_weight, inner_ton_price,
                      cover_pages, inner_pages,
                      cover_versions, inner_versions,
                      cover_color, inner_color,
                      surface_codes, binding, other_codes, tiers):
        """为阶梯数量计算成本和各客户报价"""
        cover_sheet_cost = full_area * Decimal(str(cover_weight)) / Decimal("1000") * Decimal(str(cover_ton_price)) / Decimal("1000")
        cover_books_per_full = kai * 2 // cover_pages
        cover_press = math.ceil(qty / cover_books_per_full)
        cover_spoilage = _spoilage(cover_versions, cover_press)
        cover_buy = cover_press + cover_spoilage
        cover_paper_cost = (Decimal(str(cover_buy)) * cover_sheet_cost).quantize(Decimal("1"), ROUND_CEILING)

        inner_sheet_cost = full_area * Decimal(str(inner_weight)) / Decimal("1000") * Decimal(str(inner_ton_price)) / Decimal("1000")
        inner_books_per_full = kai * 2 // inner_pages
        if inner_books_per_full < 1:
            inner_books_per_full = 1
        inner_press = math.ceil(qty / inner_books_per_full)
        inner_spoilage = _spoilage(inner_versions, inner_press)
        inner_buy = inner_press + inner_spoilage
        inner_paper_cost = (Decimal(str(inner_buy)) * inner_sheet_cost).quantize(Decimal("1"), ROUND_CEILING)

        paper_cost = cover_paper_cost + inner_paper_cost

        cover_printing_cost = Decimal(str(cover_versions)) * Decimal(str(cover_color.price_per_version))
        inner_printing_cost = Decimal(str(inner_versions)) * Decimal(str(inner_color.price_per_version))
        printing_cost = cover_printing_cost + inner_printing_cost

        surface_cost = Decimal("0")
        for code in surface_codes:
            proc = self.db.query(HuacePostProcessing).filter(
                HuacePostProcessing.code == code,
                HuacePostProcessing.proc_group == "surface",
                HuacePostProcessing.is_active == True
            ).first()
            if proc:
                raw = Decimal(str(cover_buy)) * full_area * Decimal(str(proc.unit_price))
                surface_cost += max(raw, Decimal(str(proc.min_charge)))

        binding_cost = Decimal("0")
        if binding:
            raw = Decimal(str(qty)) * Decimal(str(binding.unit_price))
            binding_cost = max(raw, Decimal(str(binding.min_charge)))

        other_cost = Decimal("0")
        for code in other_codes:
            proc = self.db.query(HuacePostProcessing).filter(
                HuacePostProcessing.code == code,
                HuacePostProcessing.proc_group == "other",
                HuacePostProcessing.is_active == True
            ).first()
            if proc:
                if proc.price_type == "per_book":
                    raw = Decimal(str(qty)) * Decimal(str(proc.unit_price))
                else:
                    raw = Decimal(str(proc.min_charge))
                other_cost += max(raw, Decimal(str(proc.min_charge)))

        total_cost = paper_cost + printing_cost + surface_cost + binding_cost + other_cost

        cost_breakdown = {
            "paper_cost": float(paper_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "printing_cost": float(printing_cost),
            "surface_cost": float(surface_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "binding_cost": float(binding_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "other_post_cost": float(other_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
            "total_cost": float(total_cost.quantize(Decimal("1"), ROUND_HALF_UP)),
        }

        tier_prices = []
        for t in tiers:
            tp = float((total_cost * Decimal(str(t.multiplier))).quantize(Decimal("0.01"), ROUND_HALF_UP))
            up = round(tp / qty, 4) if qty > 0 else 0
            tier_prices.append({
                "code": t.code,
                "name": t.name,
                "multiplier": float(t.multiplier),
                "total_price": tp,
                "unit_price": up,
            })

        return {
            "quantity": qty,
            "cost_breakdown": cost_breakdown,
            "tier_prices": tier_prices,
        }

    def _get_kai(self, size: ProductSize) -> int:
        """从 size.code 提取开数"""
        code = size.code or ""
        if "8k" in code:
            return 8
        elif "16k" in code:
            return 16
        elif "32k" in code:
            return 32
        return 16
