import json
from typing import List, Dict, Optional


STOCK = "TSLA"
TARGET_QUARTER = "2025-Q3"

def quarter_key(q: str) -> int:
    year, qtr = q.split("-Q")
    return int(year) * 4 + int(qtr)

def load_quarters(stock: str) -> List[Dict]:
    with open(f"financials/{stock}.json", "r", encoding="utf-8") as f:
        data = json.load(f)["quarters"]

    data.sort(key=lambda x: quarter_key(x["quarter"]))
    return data

def get_quarter_index(quarters, target):
    for i, q in enumerate(quarters):
        if q["quarter"] == target:
            return i
    raise ValueError(f"Quarter {target} not found")


def safe_sum(values):
    if any(v is None for v in values):
        return None
    return sum(values)


def ttm_slice(quarters, idx):
    if idx < 3:
        return None
    return quarters[idx-3:idx+1]

def find_same_quarter_last_year(quarters, quarter):
    year, qtr = quarter.split("-Q")
    target = f"{int(year)-1}-Q{qtr}"
    return next((q for q in quarters if q["quarter"] == target), None)


def calc_metrics(stock: str, quarter: str) -> Dict[str, Optional[float]]:
    qs = load_quarters(stock)
    idx = get_quarter_index(qs, quarter)

    ttm = ttm_slice(qs, idx)
    if ttm is None:
        raise ValueError("TTM requires at least 4 quarters")

    latest = qs[idx]

    # ===== TTM 基础量 =====
    ttm_revenue = safe_sum([q["revenue"] for q in ttm])
    ttm_net_income = safe_sum([q["net_income"] for q in ttm])
    ttm_gross_profit = safe_sum([q["gross_profit"] for q in ttm])
    ttm_ocf = safe_sum([q["operating_cash_flow"] for q in ttm])
    ttm_capex = safe_sum([q["capex"] for q in ttm])

    # ===== 市值 =====
    if latest["stock_price"] is None or latest["diluted_shares"] is None:
        market_cap = None
    else:
        market_cap = latest["stock_price"] * latest["diluted_shares"]

    # ===== 估值 =====
    pe = market_cap / ttm_net_income if market_cap and ttm_net_income else None
    ps = market_cap / ttm_revenue if market_cap and ttm_revenue else None
    pb = market_cap / latest["total_equity"] if market_cap and latest["total_equity"] else None

    # ===== ROE =====
    prev_equity = qs[idx-4]["total_equity"] if idx >= 4 else None
    if ttm_net_income and latest["total_equity"] and prev_equity:
        avg_equity = (latest["total_equity"] + prev_equity) / 2
        roe = ttm_net_income / avg_equity * 100
    else:
        roe = None

    # ===== 增长 =====
    yoy_q = find_same_quarter_last_year(qs, quarter) #next((q for q in qs if q["quarter"] == f"{int(quarter[:4])-1}{quarter[4:]}"), None)
    if yoy_q and latest["revenue"] and yoy_q["revenue"]:
        revenue_yoy = (latest["revenue"] - yoy_q["revenue"]) / yoy_q["revenue"] * 100
    else:
        revenue_yoy = None

    # ===== 经营质量 =====
    gross_margin = ttm_gross_profit / ttm_revenue * 100 if ttm_gross_profit and ttm_revenue else None

    if ttm_ocf and ttm_capex and ttm_revenue:
        fcf_margin = (ttm_ocf - ttm_capex) / ttm_revenue * 100
        capex_ratio = ttm_capex / ttm_revenue * 100
    else:
        fcf_margin = None
        capex_ratio = None

    return {
        "pe": pe,
        "pb": pb,
        "ps": ps,
        "roe": roe,
        "roic": latest["roic"],
        "wacc": latest["wacc"],
        "revenue_yoy": revenue_yoy,
        "gross_margin": gross_margin,
        "fcf_margin": fcf_margin,
        "capex_to_revenue": capex_ratio
    }


if __name__ == "__main__":
    result = calc_metrics(STOCK, TARGET_QUARTER)
    print(json.dumps(result, indent=2))
