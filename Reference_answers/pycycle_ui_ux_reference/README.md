# pyCycle UI/UX Reference Answer

本資料夾保存一個可執行的 PySide6 工程分析參考 app。它會執行 upstream pyCycle 的高旁通比渦扇範例、保存 pyCycle 英文 viewer 報告、解析 performance data，並與 CFM56-7B 公開資料做圖表與正體中文報告比對。

## 第一階段目標

- 使用 `uv` 管理 Python 3.12 環境與 `.venv`。
- 使用 `PySide6` 建立桌面 UI。
- 套用適合工程教學的 UI 模板與 Claude 米色風格。
- 使用 `pyqtgraph` 顯示 CFM56-7B 比對圖。
- 執行 upstream `high_bypass_turbofan.py` 的精簡 wrapper。
- 使用 Ribbon 風格操作列與工程參數輸入框。
- 使用背景 thread 執行 pyCycle，避免 UI 在求解期間停止回應。
- 產生 pyCycle 英文 viewer 報告與正體中文 Markdown 報告。

## UI 應具備的區域

- pyCycle 執行：跑 HBTF wrapper，保存 `hbtf_view.out`。
- 流程圖：進氣、風扇、壓縮機、燃燒室、渦輪、噴嘴。
- 結果摘要：Fn、TSFC、OPR、BPR。
- 圖表：pyCycle 與 CFM56-7B 參考資料比對。
- 報告：pyCycle 英文 viewer 與本 app 產生的正體中文報告。

## 啟動方式

```powershell
uv run pycycle-edu-ui
```

## 已驗證輸出

| 路徑 | 內容 |
|---|---|
| `runs/20260511-155126/hbtf_view.out` | pyCycle 英文 viewer 報告。 |
| `reports/hbtf_cfm56_7b_report_zh_20260511-155219.md` | 正體中文比對報告。 |
| `screenshots/ribbon_ui_offscreen.png` | Ribbon 介面初始畫面檢查。 |
| `screenshots/ribbon_ui_after_run.png` | 背景執行 pyCycle 後的 Ribbon UI 截圖。 |

如果需要直接從模組啟動：

```powershell
uv run python -m pycycle_edu_ui.main
```

## 第一版畫面檢查

目前已用 Qt offscreen 模式輸出檢查圖：

```text
Reference_answers/pycycle_ui_ux_reference/screenshots/main_window_offscreen.png
Reference_answers/pycycle_ui_ux_reference/screenshots/main_window_after_pycycle.png
Reference_answers/pycycle_ui_ux_reference/screenshots/ribbon_ui_offscreen.png
Reference_answers/pycycle_ui_ux_reference/screenshots/ribbon_ui_after_run.png
```
