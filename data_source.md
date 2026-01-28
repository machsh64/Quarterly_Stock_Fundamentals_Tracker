
## 数据与获取方式
### 财报获取（强制）
- revenue
- gross_profit
- net_income
- operating_cash_flow
- capex
- total_equity
- total_debt
- cash_and_equivalents
- diluted_shares

### 市场数据软件
- stock_price

### 从gurufocus获取
- roic
- wacc

## 数据源头
### 一、【公司财报（10-Q / 10-K）里一定能找到的字段】
[yahoo finance](https://finance.yahoo.com/quote/NVDA/financials/)

| 字段                    | 	去哪找                        | 	具体位置                                                                                               | 备注   
|-----------------------|-----------------------------|-----------------------------------------------------------------------------------------------------|------|
| revenue               | 	Income Statement           | 	Total Revenue (finance_yahoo: Income Statement -> Total Revenue)                                   | 	季度值 |
| gross_profit	         | Income Statement            | Gross Profit (finance_yahoo: Income Statement -> Gross Profit)                                      | 季度值  |
| net_income            | Income Statement            | Net Income (GAAP)	(finance_yahoo: Income Statement -> Net Income)                                   | 季度值  |
| operating_cash_flow	  | Cash Flow	                  | Net Cash Provided by Operating Activities (finance_yahoo: Cash Flow -> Operating Cash Flow )        | 季度值  |
| capex	                | Cash Flow	                  | Capital Expenditures	(finance_yahoo: Cash Flow -> Capital Expenditure)                              | 取正值  |
| total_equity	         | Balance Sheet	              | Total Shareholders' Equity	(finance_yahoo : Balance Sheet -> Total Equity Gross Minority Interest ) | 期末   |
| total_debt	           | Balance Sheet	              | Short + Long-term Debt	(finance_yahoo : Balance Sheet -> Total Debt )                               | 合并   |
| cash_and_equivalents	 | Balance Sheet	              | Cash And Cash Equivalents	(finance_yahoo : Cash Flow -> End Cash Position )                         | 期末   |
| diluted_shares        | Income Statement / Footnote | Diluted Weighted Average Shares (finance_yahoo : Income Statement -> Diluted Average Shares         | 季度   |


### 二、【市场数据软件中获取】

源：Yahoo / Macrotrends / Gurufocus / TIKR

| 字段           | 去哪找 | 精确口径 | 要取的值  |   
|--------------| --- | --- |----------|
| stock_price  | Yahoo Finance | Historical Prices | 季度最后一个交易日 Close |

📌 示例

- 2024-Q4 → 2024-12-31 → Close

### 三、🏦【第三方估算工具（财报里不存在）】

源：Gurufocus / Damodaran / SeekingAlpha

| 字段	| 去哪找	| 说明 |
|------|---------|------|
| roic | Gurufocus (Ratios -> ROIC%) / Damodaran | 	市场假设值 |
| wacc | Gurufocus  (Ratios -> WACC%) / Damodaran | 	市场假设值 |

📌 示例：

- "roic": 118
- "wacc": 9.5
