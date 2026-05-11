# pyCycle Edu

這個 repository 是 upstream pyCycle 的教育與工作區包裝專案。
`upstream/pyCycle` 只作為唯讀參考 submodule；教學素材、參考來源、開發日誌，以及未來要建立的 wrapper 程式，都放在 upstream 之外。

## 目前教學目標

建立一套正體中文課程，教學生如何用提示詞指揮 AI：

- 用 `uv` 與 `.venv` 管理可重現的 Python 環境。
- 把 pyCycle 範例當作唯讀參考模型。
- 將公開的發動機資料先整理並引用到 `Reference_sources/`。
- 規劃一個 PySide6 UI，逐步趨近 GasTurb 入門工作流程。
- 產生正體中文與英文工程報告，並清楚標示資料來源與模型限制。

第一個教學案例是 CFM56-7B 等級的高旁通比渦扇。課程會先使用 upstream pyCycle 的 `high_bypass_turbofan.py` 作為學習骨架；這個範例不能被宣稱為已校正的 CFM56-7B engine deck。

## 專案結構

| 路徑 | 用途 |
|---|---|
| `upstream/pyCycle/` | upstream pyCycle submodule，只能唯讀參考。除非明確要求同步 upstream，否則不得修改或更新 gitlink。 |
| `Reference_sources/` | 外部參考來源、來源清單與資料治理規則。 |
| `Reference_answers/` | 課程參考答案、階段提示詞、預期輸出與 UI/UX 參考實作說明。 |
| `src/pycycle_edu_ui/` | PySide6 教學工作台。第一版先提供 UI/UX 與教學估算，後續再接 pyCycle runner。 |
| `docs/slides/` | 教學投影片產生器、PPTX、視覺檢查預覽圖與本地圖片素材。 |
| `docs/dev-log/` | 有意義開發工作的必要紀錄。 |
| `docs/research/` | 研究目標與教學/研究進度紀錄。 |
| `docs/sessions/` | 每次工作階段的交接摘要。 |
| `scripts/` | repository 維護與驗證腳本。 |

## PySide6 UI 工作台

第一版 UI 使用 `PySide6`、`PySide6-Fluent-Widgets`、`pyqtgraph`、`OpenMDAO` 與唯讀 upstream pyCycle，並套用 Claude 類型的米色、暖色、低對比、大字級設計。

建議使用 Python 3.12。第一次安裝：

```powershell
uv sync --python 3.12
```

啟動：

```powershell
uv run pycycle-edu-ui
```

也可以從模組啟動：

```powershell
uv run python -m pycycle_edu_ui.main
```

目前 UI 已包含：

- 類 Microsoft Office Ribbon 的上方操作列：模型設定、執行計算、結果圖表、報告輸出、資料來源。
- 可輸入工程參數：Mach、Altitude、T4/Tt4、Fn target、BPR、Fan PR、LPC PR、HPC PR、Percent thrust。
- 執行 upstream `high_bypass_turbofan.py` 的精簡 wrapper。
- 背景執行 pyCycle 計算，避免 UI 在求解期間卡住。
- 解析 pyCycle 英文 viewer 報告 `hbtf_view.out`。
- 顯示 pyCycle DESIGN 與 OD performance points。
- 將 BPR、OPR、推力、TSFC 與 CFM56-7B 公開資料做表格與圖表比對。
- 產生正體中文 Markdown 報告，並保留 pyCycle 原始英文 viewer 報告。

輸出位置：

| 路徑 | 用途 |
|---|---|
| `Reference_answers/pycycle_ui_ux_reference/runs/` | 每次 pyCycle 執行的英文 viewer 報告。 |
| `Reference_answers/pycycle_ui_ux_reference/reports/` | 正體中文比對報告。 |
| `Reference_answers/pycycle_ui_ux_reference/screenshots/` | UI 檢查截圖。 |

注意：目前 app 使用 pyCycle HBTF 範例與 CFM56-7B 公開資料做工程等級比對；這仍不能宣稱為已完成 CFM56-7B 原廠 engine deck 校正。

## 目前投影片

目前的課程規劃投影片：

```text
docs/slides/pycycle_ai_prompting_course.pptx
```

產生方式：

```powershell
uv run --with python-pptx --with pillow python docs/slides/build_pycycle_ai_prompting_ppt.py
```

每次產生或更新 PPTX 後，必須匯出成圖片檢查版面：

```powershell
./docs/slides/export-pptx-preview.ps1
```

檢查重點：

- 文字不得跑出框線或被裁切。
- 圖片必須等比例呈現，不可被拉寬或壓扁。
- 投影用字級需足夠大，需考量年長學生或遠距投影環境。
- 圖文比例要平衡，不能只有文字。

## 必要工作流程

分析或修改前，先執行：

```powershell
npx gitnexus analyze --embeddings
```

提交前，先執行：

```powershell
./scripts/verify-upstream-submodule.ps1
```

每次有意義的工作，都要記錄在 `docs/dev-log/`。

## 固定收尾流程

每次完成一個版本或階段時，依序判斷並處理：

0. Commit 並推送。
1. 根據版本判斷是否更新版本。
2. 根據版本判斷是否發布新 Release。
3. 根據版本判斷是否更新或新增 `docs/` 裡的 Markdown。
4. 根據版本判斷是否更新 `README.md`。
5. 根據版本判斷是否更新 `CLAUDE.md` 與 `AGENTS.md`。
6. 根據版本判斷是否更新或新增 `docs/` 裡的 Markdown。
7. 根據版本判斷是否照規則更新開發者日誌並新增 session。
8. 根據版本判斷是否更新研究目標和日誌。

## 版本與 Release

目前專案還沒有版本檔、tag 規範或 Release policy。
目前工作屬於教材與文件準備，因此需要 commit/push，但不需要發 GitHub Release；若未來加入版本規則，再依規則判斷是否發布 Release。
