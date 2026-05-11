# 2026-05-11 PySide6 UI/UX 研究與目標

## 研究目標

建立一個以 PySide6 實作的 pyCycle Edu 工作台，讓學生能用提示詞逐步要求 AI：

- 建立 `uv` 與 `.venv` 管理流程。
- 查證並保存公開發動機資料。
- 使用 pyCycle 範例建立單軸高旁通比渦扇教學案例。
- 產生接近 GasTurb 入門流程的參數、圖表與報告介面。

## 模板選擇

第一階段採用 `PySide6 + QFluentWidgets / Qt Widgets fallback + pyqtgraph`。

選擇理由：

- PySide6 是 Qt 官方 Python binding。
- QFluentWidgets 提供現代桌面軟體常見的導覽與表單元件。
- pyqtgraph 適合工程與科學圖表。
- 自訂 QSS 可套用 Claude 米色、暖色與低對比風格，並把字級調大以利教學投影。

## 分階段實作

1. 建立 UI shell、參數表單、流程圖、結果卡片與雙語報告草稿。
2. 將教學估算模型替換為 pyCycle wrapper。
3. 將 `Reference_sources/` 的公開資料與 pyCycle 結果做比對。
4. 匯出正體中文與英文報告。

## 注意事項

- `upstream/pyCycle` 仍是唯讀 submodule。
- 第一版 UI 的數值是教學估算，不能宣稱已完成 CFM56-7B 校正。
- 真實驗證需在後續階段加入 pyCycle runner、來源對照與誤差表。
