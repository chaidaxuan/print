"""
画册报价引擎对拍测试（无需 MySQL，用 stub DB）

基准样例（memory/huace-calc-logic.md，已对参考站验算到元）：
  大度16开285×210，封面双铜80克/4P/四色，内页双铜80克/16P/四色，1000本
  纸款771 + 印刷1250 + 表面处理102 + 骑马钉100 = 成本2223，单价2.223
"""
import sys
from types import SimpleNamespace

# 控制台可能是 GBK，计算轨迹里含 ⌈⌉ 等字符，强制 UTF-8 输出避免崩溃
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from app.services.huace_engine import HuaceQuoteEngine


class FakeQuery:
    """模拟 SQLAlchemy Query：按 model + filter 条件返回预置对象"""

    def __init__(self, store, model):
        self._store = store
        self._model = model
        self._filters = []

    def filter(self, *conditions):
        # 只按等值条件粗筛：解析 BinaryExpression 的右值
        for c in conditions:
            try:
                col = c.left.key
                val = c.right.value
                self._filters.append((col, val))
            except AttributeError:
                pass  # is_active == True 之类，忽略
        return self

    def order_by(self, *args):
        return self

    def _matches(self, obj):
        for col, val in self._filters:
            if getattr(obj, col, None) != val:
                return False
        return True

    def first(self):
        for obj in self._store.get(self._model, []):
            if self._matches(obj):
                return obj
        return None

    def all(self):
        return [o for o in self._store.get(self._model, []) if self._matches(o)]


class FakeDB:
    def __init__(self, store):
        self._store = store

    def query(self, model):
        return FakeQuery(self._store, model)


def build_store():
    from app.models import ProductSize
    from app.models.huace_color import HuaceColorPrice
    from app.models.huace_binding import HuaceBinding
    from app.models.huace_post_processing import HuacePostProcessing
    from app.models.huace_client_tier import HuaceClientTier

    size = SimpleNamespace(id=1, code="dadu_16k", name="大度16开")

    cover_cmyk = SimpleNamespace(component="cover", color_code="cmyk",
                                 price_per_version=250, is_active=True)
    inner_cmyk = SimpleNamespace(component="inner", color_code="cmyk",
                                 price_per_version=250, is_active=True)

    saddle = SimpleNamespace(code="saddle_stitch", name="骑马钉",
                             price_type="per_book", unit_price=0.10,
                             min_charge=0, is_active=True)

    film_gloss = SimpleNamespace(code="film_gloss", name="过光膜",
                                 proc_group="surface", price_type="per_area",
                                 unit_price=0.40, min_charge=100, is_active=True)

    tiers = [
        SimpleNamespace(code="cost", name="成本价", multiplier=1.0, sort_order=1, is_active=True),
        SimpleNamespace(code="cash", name="现金客户", multiplier=1.15, sort_order=2, is_active=True),
    ]

    return {
        ProductSize: [size],
        HuaceColorPrice: [cover_cmyk, inner_cmyk],
        HuaceBinding: [saddle],
        HuacePostProcessing: [film_gloss],
        HuaceClientTier: tiers,
    }


def main():
    db = FakeDB(build_store())
    engine = HuaceQuoteEngine(db)

    params = {
        "size_id": 1,
        "quantity": 1000,
        "cover_paper_name": "双铜纸",
        "cover_paper_weight": 80,
        "cover_paper_ton_price": 12800,
        "cover_pages": 4,
        "cover_color_code": "cmyk",
        "inner_paper_name": "双铜纸",
        "inner_paper_weight": 80,
        "inner_paper_ton_price": 12800,
        "inner_pages": 16,
        "inner_color_code": "cmyk",
        "binding_code": "saddle_stitch",
        "surface_treatment": "film_gloss",
        "other_processing": [],
        "multi_quantities": [],
    }

    result = engine.calculate(params)
    cb = result["cost_breakdown"]

    expected = {
        "paper_cost": 771,
        "printing_cost": 1250,
        "surface_cost": 102,
        "binding_cost": 100,
        "total_cost": 2223,
    }

    print("=== 画册基准对拍（大度16开 / 1000本）===")
    print(f"{'项目':<12}{'实算':>10}{'参考':>10}{'差异':>8}")
    all_ok = True
    for k, exp in expected.items():
        got = cb[k]
        diff = got - exp
        flag = "OK" if abs(diff) <= 2 else "FAIL"
        if flag == "FAIL":
            all_ok = False
        print(f"{k:<12}{got:>10}{exp:>10}{diff:>8}  {flag}")

    print()
    print("=== 计算轨迹 ===")
    for step in result["calc_trace"]:
        print(f"  {step['label']}: {step['substituted']} = {step['result']}{step.get('unit','')}")

    print()
    print("=== 客户报价 ===")
    for tp in result["tier_prices"]:
        print(f"  {tp['name']}: 总价{tp['total_price']} 单价{tp['unit_price']}")

    print()
    print("整体在 ±2元 容差内通过" if all_ok else "存在超差项，需校准")
    return all_ok


if __name__ == "__main__":
    ok = main()
    raise SystemExit(0 if ok else 1)
