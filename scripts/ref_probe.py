"""
参考站(yinshuabaojia.com 演示 265)专版联单接口直连探针。

关键认证细节（踩坑记录）：
- body 必须是表单字段 myPara=<URL编码的JSON>，不是原始 JSON。
- CustomerPassword 用会话令牌(mscpassword)，不是 URL 里那个。
- 令牌在登录后的 cookie 里；也可从已打开的报价页全局变量 pCustomerPassword 抓。
- 请求路径要带 ASP.NET cookieless 会话段 (S(xxx))。

用法：把浏览器里抓到的 SESSION / PWD 填进来（会话会过期，过期就重开报价页再抓一次），
之后纯 requests 循环，速度远快于 Playwright 每次 eval。
"""
import json
import time
import ssl
import sys
import io
import urllib.request
import urllib.parse

# Windows 控制台按 UTF-8 输出，避免中文乱码。
# 仅在作为主脚本运行时重设；被 import 时不动 stdout，避免关掉调用方共享的 buffer。
def _force_utf8_stdout():
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
    except Exception:
        pass

# —— 从浏览器会话抓来的三要素（过期需更新）——
SESSION = "(S(0hs53n0s5we505rgcikfcvld))"
PWD = "0E47B4267F98296001DD7145F86A80896DD73BABBB197633"
CUSTOMER = "265"
HOST = "https://baojia.yinshuabaojia.com:8000"

COOKIE = (
    f"OneCustomerId{CUSTOMER}={CUSTOMER}; "
    f"mscuser{CUSTOMER}=1708888; "
    f"mscpassword{CUSTOMER}={PWD}; "
    f"isremeberme{CUSTOMER}=true; "
    f"mscuserid{CUSTOMER}={CUSTOMER}"
)

_ctx = ssl.create_default_context()
_ctx.check_hostname = False
_ctx.verify_mode = ssl.CERT_NONE


def _base(**over):
    b = {
        "ClientType": 0, "ProvinceId": -1, "CityId": -1, "QuotePriceSupplier": CUSTOMER,
        "CustomerId": CUSTOMER, "CustomerPassword": PWD, "CustomerId2": CUSTOMER,
        "QuotePriceId": 16, "IsGetMoreQuote": True, "OtherList": [],
        "OtherPost": [{"F_OtherPostId": "0", "F_OtherPostLength": "1", "F_OtherPostWidth": "1",
                       "F_OtherPostQty": "1", "F_OtherPostSizeLength": "1", "F_OtherPostSetQty": "1"}],
        "F_ColorBoxTypeId": "1", "F_NormarlSizeType": "34", "Qty": "100", "F_Copies": "3",
        "F_OneSheetPages": "99", "F_ColorId1": "1", "F_PaperWeight": "50",
        "F_CustomerSelect": "", "F_ProductName": "",
        "MultiQty1": "100", "F_CustomExpress": "0", "MultiQty2": "200", "MultiExpress2": "0",
        "MultiQty3": "300", "MultiExpress3": "0", "MultiQty4": "400", "MultiExpress4": "0",
        "MultiQty5": "500", "MultiExpress5": "0",
        "F_PostprocessingQty": 0, "F_PostprocessingQty2": 0,
        "F_IsPaste": True, "F_IsPasteLeft": True, "CustomerPost": [],
    }
    b.update(over)
    return b


def _post(path, body_str, content_type):
    url = f"{HOST}/{SESSION}/{path}"
    req = urllib.request.Request(
        url, data=body_str.encode("utf-8"),
        headers={
            "Content-Type": content_type,
            "Cookie": COOKIE,
            "Referer": f"{HOST}/{SESSION}/QuotePrice_new.aspx?QuoteItemId=16&OneId={CUSTOMER}",
            "User-Agent": "Mozilla/5.0",
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    with urllib.request.urlopen(req, context=_ctx, timeout=30) as r:
        return r.read().decode("utf-8")


def quote(**over):
    payload = _base(**over)
    body = "myPara=" + urllib.parse.quote(json.dumps(payload))
    txt = _post(f"ashx/YouXiaoQuotePrice.ashx?date={int(time.time()*1000)}",
                body, "application/x-www-form-urlencoded")
    return json.loads(txt)


def detail(log_id):
    para = {"LogId": log_id, "SupplierId": CUSTOMER, "Password": PWD}
    body = "myPara=" + urllib.parse.quote(json.dumps(para))
    txt = _post(f"ashx/com_GetLogInfo.ashx?callback=cb", body,
                "application/x-www-form-urlencoded")
    # jsonp: cb(...)
    s, e = txt.find("("), txt.rfind(")")
    return json.loads(txt[s + 1:e])


def line_items(log_id):
    """返回明细分项：纸款/印刷费/后加工/生产成本/成本附加/总成本 + 印张/机器/色数。"""
    d = detail(log_id)
    L = d["Log"]
    sheets = machine = color_qty = None
    for ld in d.get("LogDetails", []):
        det = ld.get("Details") or {}
        if "印刷" in (det.get("F_Info") or ""):
            sheets = det.get("F_OnMachineNum")
            machine = det.get("F_MachineName")
            color_qty = det.get("F_ColorQty")
            break
    return {
        "纸款": L["F_PaperAmt"], "印刷费": L["F_PrintAmt"], "后加工": L["F_PostProcessingAmt"],
        "生产成本": L["F_CostNotProfit"], "成本附加": L["F_ProfitAmt"], "总成本": L["F_Cost"],
        "印张": sheets, "机器": machine, "色数": color_qty,
    }


if __name__ == "__main__":
    _force_utf8_stdout()
    # 冒烟测试：直连能否打通 + 单黑基准分项
    res = quote(F_ColorId1="1")
    print("Result:", res.get("Result"), "Err:", res.get("ErrorMessage"),
          "CostList:", res.get("CostList"))
    if not res.get("Result"):
        sys.exit("会话可能过期，重开报价页抓新 SESSION/PWD")

    # 实验A：单黑多数量，解开机费 + 印工斜率（印刷费 = 开机 + 印张/1000 × 千印价）
    print("\n=== A. 单黑多数量（解 开机费/千印价）===")
    rows = []
    for q in ["100", "200", "300", "500", "1000", "2000", "5000"]:
        r = quote(F_ColorId1="1", Qty=q, MultiQty1=q, MultiQty2=q,
                  MultiQty3=q, MultiQty4=q, MultiQty5=q)
        li = line_items(r["LogId"])
        rows.append((int(q), li["印张"], li["印刷费"]))
        print(f"  数量{q:>5}  印张{li['印张']:>7}  印刷费{li['印刷费']:>7}")
        time.sleep(0.15)
    # 用首末两点解线性 印刷费 = a + b×印张
    (q0, s0, p0), (q1, s1, p1) = rows[0], rows[-1]
    b = (p1 - p0) / (s1 - s0)
    a = p0 - b * s0
    print(f"  → 拟合 印刷费 = {a:.2f} + {b*1000:.3f}/千张 × 印张")
    for q, s, p in rows:
        fit = a + b * s
        print(f"     校验 数量{q:>5} 实际{p:>7} 拟合{fit:8.1f} 差{p-fit:+.1f}")

    # 实验B：彩色 vs 专色的加价结构（固定档 vs 线性）
    print("\n=== B. 各颜色印刷费（100 与 500 两档，看固定/线性）===")
    color_names = {"1": "单黑", "2": "双色", "3": "四色", "4": "1专色",
                   "5": "2专色", "6": "3专色", "7": "4专色",
                   "8": "彩+1专", "11": "彩+4专"}
    for q in ["100", "500"]:
        print(f"  -- 数量 {q} --")
        for c, nm in color_names.items():
            r = quote(F_ColorId1=c, Qty=q, MultiQty1=q, MultiQty2=q,
                      MultiQty3=q, MultiQty4=q, MultiQty5=q)
            li = line_items(r["LogId"])
            print(f"     {nm:<6} 色数{li['色数']}  印张{li['印张']:>7}  印刷费{li['印刷费']:>7}")
            time.sleep(0.15)
