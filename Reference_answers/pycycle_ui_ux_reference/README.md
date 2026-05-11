# pyCycle UI/UX Reference Answer

本參考答案示範如何要求 AI 協助建立一個 PySide6 UI/UX，逐步趨近 GasTurb 入門工作流程，但仍保留 pyCycle 的開源與可追蹤特性。

## 第一階段目標

- 使用 `uv` 管理 Python 環境與 `.venv`。
- 使用 `PySide6` 建立桌面 UI。
- 套用適合工程教學的 UI 模板與 Claude 米色風格。
- 使用 `pyqtgraph` 預留工程圖表。
- 建立單軸高旁通比渦扇的教學參數畫面。
- 先用教學估算模型驗證 UI 流程，下一階段再接 pyCycle runner。

## UI 應具備的區域

- 發動機設定：BPR、OPR、Tt4、高度、馬赫數、質量流率。
- 流程圖：進氣、風扇、壓縮機、燃燒室、渦輪、噴嘴。
- 結果摘要：淨推力、TSFC、燃油流量、推進效率。
- 圖表：旁通比掃描、壓比掃描。
- 報告：正體中文與英文摘要。

## 啟動方式

```powershell
uv run pycycle-edu-ui
```

如果需要直接從模組啟動：

```powershell
uv run python -m pycycle_edu_ui.main
```

## 第一版畫面檢查

目前已用 Qt offscreen 模式輸出一張初步檢查圖：

```text
Reference_answers/pycycle_ui_ux_reference/screenshots/main_window_offscreen.png
```
