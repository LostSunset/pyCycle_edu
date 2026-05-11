# 2026-05-11 PySide6 UI/UX Session

## Summary

本階段開始建立 pyCycle Edu 的 PySide6 UI/UX 參考實作，並依使用者修正要求改為真正可用的 pyCycle reference app。

## User Requirements

- 建立參考答案資料夾。
- 開始實作用 PySide6 為 pyCycle 建立 UI/UX。
- 先上網找最適合的 UI/UX 模板並套用。
- UI 需延續 Claude 米色與圖案風格。
- 不修改 upstream pyCycle。

## Decisions

- 使用 `PySide6 + QFluentWidgets / Qt Widgets fallback + pyqtgraph`。
- Reference app 必須跑真實 pyCycle wrapper，不使用教學估算當主要結果。
- 保存 pyCycle 原始英文 viewer 報告，另由 app 產生正體中文報告。
- 將 CFM56-7B 公開資料與 pyCycle BPR、OPR、Fn、TSFC 做表格與圖表比對。
- UI 改為 Ribbon 風格，並加入 Mach、Altitude、T4/Tt4、Fn target、BPR、Fan PR、LPC PR、HPC PR、Percent thrust 輸入框。
- pyCycle 計算改由背景 thread 執行，狀態列顯示執行狀態、耗時與輸出路徑。
- 參考答案放在 `Reference_answers/`。

## Next Steps

- 增加更多同工況 CFM56-7B 資料來源後，再做嚴格誤差比較。
- 加入 PDF/HTML 報告輸出。
