# 2026-05-11 PySide6 UI/UX Session

## Summary

本階段開始建立 pyCycle Edu 的 PySide6 UI/UX 參考實作。

## User Requirements

- 建立參考答案資料夾。
- 開始實作用 PySide6 為 pyCycle 建立 UI/UX。
- 先上網找最適合的 UI/UX 模板並套用。
- UI 需延續 Claude 米色與圖案風格。
- 不修改 upstream pyCycle。

## Decisions

- 使用 `PySide6 + QFluentWidgets / Qt Widgets fallback + pyqtgraph`。
- 第一版 UI 顯示單軸高旁通比渦扇教學估算，下一階段再接 pyCycle runner。
- 參考答案放在 `Reference_answers/`。

## Next Steps

- 將 UI 參數接到 pyCycle wrapper。
- 建立可重現的 pyCycle 執行與結果擷取。
- 加入報告輸出檔案功能。
