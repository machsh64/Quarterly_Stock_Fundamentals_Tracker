# Quarterly Stock Fundamentals Tracker

一个轻量级的 Python 工具，用于从季度财报（10-Q/10-K）和外部数据源（GuruFocus 等）计算股票的关键基本面指标，支持 TTM（Trailing Twelve Months）计算。适用于价值投资筛选、量化回测、个人股票跟踪仪表盘等场景。

当前支持的指标（以目标季度为基础）：
- **估值**：PE（TTM）、PB、PS（TTM）
- **盈利与资本效率**：ROE（TTM）、ROIC（GuruFocus）、WACC（GuruFocus）
- **增长与经营质量**：收入同比 YoY（%）、毛利率（TTM）、自由现金流率（TTM）
- **资本投入**：CapEx / 收入（TTM）

## 核心特性

- 基于标准化的季度 JSON 数据自动计算 TTM 指标
- 安全处理缺失值（None），避免除零错误
- ROIC 和 WACC 优先直接使用 GuruFocus 的历史季度值，确保一致性和准确性
- 支持任意目标季度计算（例如 "2024-Q4"）
- 输出结构化 JSON，便于后续分析、绘图或导入 Excel

## 数据来源

| 数据类别             | 来源                              | 说明                                                                 |
|----------------------|-----------------------------------|----------------------------------------------------------------------|
| 收入、毛利、净利润   | SEC 10-Q / 10-K（Income Statement） | 直接从财报原始数据获取                                               |
| 经营现金流、CapEx    | SEC 10-Q / 10-K（Cash Flow Statement） | 经营活动现金流净额、资本支出（负值取绝对值）                         |
| 总权益、总债务、现金 | SEC 10-Q / 10-K（Balance Sheet）   | 股东权益总额、短期+长期债务、现金及等价物                             |
| 稀释股数             | 财报 EPS 计算部分或注脚           | Diluted weighted average shares outstanding                          |
| 季度末收盘价         | Yahoo Finance / Bloomberg 等      | 对应季度最后交易日收盘价                                             |
| ROIC                 | GuruFocus                         | 历史季度 ROIC 值（%）                                                |
| WACC                 | GuruFocus                         | 历史季度/年度 WACC 值（%）                                           |

## 数据准备
在项目 financials/ 文件夹，放入以股票代码命名的 JSON 文件，例如 financials/TSLA.json。
JSON 结构示例（financials/TSLA.json）：
```json
{
  "stock": "TSLA",
  "quarters": [
    {
      "quarter": "2023-Q4",
      "revenue": 25167,
      "gross_profit": 4540,
      "net_income": 2064,
      "operating_cash_flow": 4350,
      "capex": 2346,
      "total_equity": 65000,
      "total_debt": 9200,
      "cash_and_equivalents": 27000,
      "diluted_shares": 3180,
      "stock_price": 248,
      "wacc": 9.5,
      "roic": 12.8
    },
    {
      "quarter": "2024-Q4",
      "revenue": 25167,
      "gross_profit": 4800,
      "net_income": 2064,
      "operating_cash_flow": 4350,
      "capex": 2346,
      "total_equity": 69800,
      "total_debt": 9900,
      "cash_and_equivalents": 31000,
      "diluted_shares": 3205,
      "stock_price": 240,
      "wacc": 9.5,
      "roic": 13.4
    }
  ],
  "data_sources": {
    "financials": "Tesla 10-K / 10-Q",
    "stock_price": "Yahoo Finance (quarter-end close)",
    "wacc": "GuruFocus",
    "roic": "GuruFocus"
  }
}
```

注意：
- 数值单位建议统一（例如百万美元），但程序不强制
- 每个 quarter 必须包含 "quarter" 字段（格式：YYYY-Q[1-4]）
- roic 和 wacc 必须从 GuruFocus 填写（强烈推荐）

## 数据获取途径
1. 参考 data_source.md 文件内描述获取（推荐）
2. 通过 prompt.txt 从具有检索功能的模型获取

## 使用说明
```bash
# 基本用法（命令行运行）
python ttm_engine.py --stock TSLA --quarter 2024-Q4
```

示例输出（JSON 格式）：
```json
{
  "pe": 117.92,
  "pb": 11.02,
  "ps": 8.12,
  "roe": 9.68,
  "roic": 13.4,
  "wacc": 9.5,
  "revenue_yoy": 0.0,
  "gross_margin": 18.78,
  "fcf_margin": 7.24,
  "capex_to_revenue": 9.84
}
```
