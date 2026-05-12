# pyCycle_GUI

[正體中文](#正體中文) | [English](#english)

## 正體中文

`pyCycle_GUI` 是圍繞 upstream pyCycle 建立的專業教學與工作區。
**v0.2.0** 提供第一個給終端使用者操作的教學範例：獨立的簡易單軸渦輪噴射引擎
PySide6 GUI，並附有雙語使用者文件。

`upstream/pyCycle` 是唯讀參考 submodule。除非明確要求同步 upstream，
否則不要修改其中檔案，也不要更新 gitlink 指標。

### 目前狀態

- **教學 GUI（v0.2.0 新增）：** `tutorials/simple_turbojet/simple_turbojet.py`
  — PySide6 GUI，會在 worker thread 中執行 pyCycle `MPTurbojet` 模型，
  顯示內嵌 T-S / P-h / Comparison 圖表，並將所有產物
  （TXT、PDF、PNG、HTML）寫入同一個 `output/` 資料夾。
- **雙語使用者指南：** `tutorials/simple_turbojet/README.md` — 說明如何從工程情境閱讀
  `inputs.html` 與 `n2.html`。
- **Workbench package：** `src/pycycle_edu_ui/` — runner 與雙語報告/PDF 產生工具。
  互動式 Ribbon/HBTF UI shell 已暫時退役，等待重新設計。
- **參考資源：** CFM56-7B 參考資料封存在 `Reference_sources/`。

### 環境

請先安裝必要工具：

1. 安裝 Git 與 GitHub CLI，並登入 GitHub。

   ```powershell
   winget install --id Git.Git -e
   winget install --id GitHub.cli -e
   gh auth login
   ```

   下載連結：<https://git-scm.com/downloads>、<https://cli.github.com/>

2. 安裝 `uv`，再用 `uv` 搭配 Python 3.12 建立本專案的 `.venv`。

   ```powershell
   winget install --id astral-sh.uv -e
   ```

   下載連結：<https://docs.astral.sh/uv/getting-started/installation/>

3. 安裝 Visual Studio Code Insiders。

   ```powershell
   winget install --id Microsoft.VisualStudioCode.Insiders -e
   ```

   下載連結：<https://code.visualstudio.com/insiders/>

本專案使用 `uv` 管理 Python 3.12。

```powershell
uv venv --python 3.12 --clear .venv
uv sync --python 3.12
uv pip install PySide6  # tutorial GUI 需要
```

本專案只應使用 `.venv`。

### 啟動簡易渦輪噴射 GUI

```powershell
$env:PYTHONPATH = "D:\45_pyCycle_GUI\upstream\pyCycle;D:\45_pyCycle_GUI\tutorials\simple_turbojet"
python D:\45_pyCycle_GUI\tutorials\simple_turbojet\simple_turbojet.py
```

按下 **▶ Run** 後，所有檔案會輸出到 `tutorials/simple_turbojet/output/`。
完整操作說明請見 [tutorial README](tutorials/simple_turbojet/README.md)，其中包含
`inputs.html` 與 OpenMDAO `n2.html` N² 圖的完整導讀。

### Repository 結構

| 路徑 | 用途 |
|---|---|
| `upstream/pyCycle/` | 唯讀 upstream pyCycle submodule。 |
| `tutorials/simple_turbojet/` | **獨立教學 GUI + 雙語使用者指南。** |
| `tutorials/simple_turbojet/output/` | 產生的輸出檔案（gitignored）。 |
| `src/pycycle_edu_ui/runner/` | 驅動 pyCycle cases 的 headless runners。 |
| `src/pycycle_edu_ui/simple_turbojet_report.py` | 雙語報告/PDF 產生器。 |
| `Reference_sources/` | 封存的外部參考來源。 |
| `docs/dev-log/` | 必填開發紀錄。 |
| `docs/sessions/` | 每次工作階段的 hand-off notes。 |
| `docs/research/` | 研究目標與進度紀錄。 |
| `docs/slides/` | 教學投影片產生器與 PPTX 輸出。 |
| `scripts/` | Repository 維護與驗證腳本。 |
| `CHANGELOG.md` | 版本紀錄（semver）。 |

### 教學 GUI 產生的輸出

每次執行都會在 `tutorials/simple_turbojet/output/` 重新產生：

| 檔案 | 用途 |
|---|---|
| `simple_turbojet_summary.txt` / `.pdf` | 輸入、solver log、性能摘要。 |
| `simple_turbojet_ts_diagram.png` / `.pdf` | 溫度-熵循環圖。 |
| `simple_turbojet_ph_diagram.png` / `.pdf` | 壓力-焓循環圖。 |
| `simple_turbojet_comparison.png` / `.pdf` | DESIGN vs OD0 vs OD1 四面板比較。 |
| `simple_turbojet_compressor_map_DESIGN_*.png` / `.pdf` | 含操作點的壓縮機 map。 |
| `simple_turbojet_turbine_map_DESIGN_*.png` / `.pdf` | 含操作點的渦輪 map。 |
| `DESIGN.comp.pdf` / `DESIGN.turb.pdf` | pyCycle component summary PDFs。 |
| `inputs.html` | OpenMDAO input variable inventory。 |
| `n2.html` | OpenMDAO 互動式 N² 系統結構圖。 |

### 必要工作流程

提交前請執行：

```powershell
./scripts/verify-upstream-submodule.ps1
```

每個有意義的開發任務都必須記錄在 `docs/dev-log/`。

### 版本

本專案遵循 [Semantic Versioning](https://semver.org/spec/v2.0.0.html)。
完整紀錄請見 `CHANGELOG.md`。目前版本：**0.2.0**。

## English

`pyCycle_GUI` is a professional workspace around upstream pyCycle.
**v0.2.0** ships the first end-user tutorial: a self-contained PySide6 GUI
for a simple single-spool turbojet, with bilingual user documentation.

`upstream/pyCycle` is a read-only reference submodule. Do not edit files inside
it or update its gitlink unless explicitly requested.

### Current State

- **Tutorial GUI (new in v0.2.0):** `tutorials/simple_turbojet/simple_turbojet.py`
  — PySide6 GUI that runs the pyCycle `MPTurbojet` model in a worker thread,
  shows embedded T-S / P-h / Comparison charts, and writes every artefact
  (TXT, PDF, PNG, HTML) into a single `output/` folder.
- **Bilingual user guide:** `tutorials/simple_turbojet/README.md` — covers how
  to read `inputs.html` and `n2.html` with engineering scenarios.
- **Workbench package:** `src/pycycle_edu_ui/` — runner + bilingual
  report/PDF generation. The interactive Ribbon/HBTF UI shell has been
  retired pending redesign.
- **Reference assets:** archived CFM56-7B reference material remains in
  `Reference_sources/`.

### Environment

Install the required tools first:

1. Install Git and GitHub CLI, then sign in to GitHub.

   ```powershell
   winget install --id Git.Git -e
   winget install --id GitHub.cli -e
   gh auth login
   ```

   Download links: <https://git-scm.com/downloads>, <https://cli.github.com/>

2. Install `uv`, then use it to create this project's `.venv` with Python 3.12.

   ```powershell
   winget install --id astral-sh.uv -e
   ```

   Download link: <https://docs.astral.sh/uv/getting-started/installation/>

3. Install Visual Studio Code Insiders.

   ```powershell
   winget install --id Microsoft.VisualStudioCode.Insiders -e
   ```

   Download link: <https://code.visualstudio.com/insiders/>

Use Python 3.12 through `uv`.

```powershell
uv venv --python 3.12 --clear .venv
uv sync --python 3.12
uv pip install PySide6  # required for the tutorial GUI
```

Only `.venv` should be used for this project.

### Launch the Simple Turbojet GUI

```powershell
$env:PYTHONPATH = "D:\45_pyCycle_GUI\upstream\pyCycle;D:\45_pyCycle_GUI\tutorials\simple_turbojet"
python D:\45_pyCycle_GUI\tutorials\simple_turbojet\simple_turbojet.py
```

After pressing **▶ Run**, all files appear under
`tutorials/simple_turbojet/output/`. See the [tutorial README](tutorials/simple_turbojet/README.md)
for a full walkthrough of every output file, including a complete guide to
`inputs.html` and the OpenMDAO `n2.html` N² diagram.

### Repository Structure

| Path | Purpose |
|---|---|
| `upstream/pyCycle/` | Read-only upstream pyCycle submodule. |
| `tutorials/simple_turbojet/` | **Standalone tutorial GUI + bilingual user guide.** |
| `tutorials/simple_turbojet/output/` | Generated artefacts (gitignored). |
| `src/pycycle_edu_ui/runner/` | Headless runners that drive pyCycle cases. |
| `src/pycycle_edu_ui/simple_turbojet_report.py` | Bilingual report/PDF generator. |
| `Reference_sources/` | Archived external reference sources. |
| `docs/dev-log/` | Required development log entries. |
| `docs/sessions/` | Per-session hand-off notes. |
| `docs/research/` | Research goals and progress logs. |
| `docs/slides/` | Teaching deck generator and PPTX outputs. |
| `scripts/` | Repository maintenance and verification scripts. |
| `CHANGELOG.md` | Version history (semver). |

### Outputs Produced by the Tutorial GUI

Every run regenerates these inside `tutorials/simple_turbojet/output/`:

| File | Purpose |
|---|---|
| `simple_turbojet_summary.txt` / `.pdf` | Inputs, solver log, performance summary. |
| `simple_turbojet_ts_diagram.png` / `.pdf` | Temperature-entropy cycle. |
| `simple_turbojet_ph_diagram.png` / `.pdf` | Pressure-enthalpy cycle. |
| `simple_turbojet_comparison.png` / `.pdf` | DESIGN vs OD0 vs OD1 four-panel. |
| `simple_turbojet_compressor_map_DESIGN_*.png` / `.pdf` | Compressor map with op point. |
| `simple_turbojet_turbine_map_DESIGN_*.png` / `.pdf` | Turbine map with op point. |
| `DESIGN.comp.pdf` / `DESIGN.turb.pdf` | pyCycle component summary PDFs. |
| `inputs.html` | OpenMDAO input variable inventory. |
| `n2.html` | OpenMDAO interactive N² system structure diagram. |

### Required Workflow

Before committing, run:

```powershell
./scripts/verify-upstream-submodule.ps1
```

Every meaningful development task must be recorded in `docs/dev-log/`.

### Versioning

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
See `CHANGELOG.md` for the full history. Current version: **0.2.0**.
