---
name: excel-data-processor
description: 專門用於處理 Excel (.xlsx, .xls) 和 CSV 檔案。當使用者要求分析表格、合併數據或生成報表時調用。
---

# Excel 數據處理專家

## 核心任務
- 讀取 Excel 檔案並識別結構（Header, Rows）。
- 執行數據清洗（去重、補缺、格式轉換）。
- 進行統計分析（求和、平均、同比、環比）。

## 執行流程
1. **環境檢查**：確認專案中是否已安裝 `pandas` 與 `openpyxl`。
2. **數據載入**：使用 Python 腳本讀取檔案。
3. **邏輯執行**：根據用戶需求生成對應的 DataFrame 操作邏輯。
4. **驗證與導出**：將結果保存為新的 Excel 檔案，並提供摘要報告。

## 約束
- 不得修改原始檔案，必須產出新檔案（例如：`result_timestamp.xlsx`）。
- 處理超過 10 萬列的大型檔案時，應優先考慮分批讀取或使用 `duckdb`。