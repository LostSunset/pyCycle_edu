# Simple Turbojet 教學說明（詳細版）

本目錄是 pyCycle 簡易渦輪噴射引擎（single-spool turbojet）的互動教學模組。
執行 `simple_turbojet.py` 會開啟 PySide6 圖形介面，輸入設計點參數（高度、馬赫數、
目標推力等），即可計算設計點與兩個離設計點（off-design）的循環，並把所有結果
寫到 `output/` 子資料夾。

> **若要找特定縮寫、單位、元件參數的中英對照表**，請直接打開
> [`reference.html`](./reference.html)（自含 CSS 的離線參考手冊）。本 README 著重
> 在「工程上如何使用」與「實際讀懂 inputs.html / n2.html」的流程。

---

## 目錄

1. [快速開始](#快速開始)
2. [GUI 工作流程詳解](#gui-工作流程詳解)
3. [渦輪噴射熱力學速覽](#渦輪噴射熱力學速覽)
4. [流動站位與物理意義](#流動站位與物理意義)
5. [GUI 輸入欄位逐項解釋](#gui-輸入欄位逐項解釋)
6. [`output/` 完整內容速查](#output-完整內容速查)
7. [`inputs.html` 完整解讀](#inputshtml-完整解讀)
8. [`n2.html` 完整解讀](#n2html-完整解讀)
9. [工程實務應用情境](#工程實務應用情境)
10. [收斂與環境問題排除](#收斂與環境問題排除)
11. [常見問題 FAQ](#常見問題-faq)
12. [延伸閱讀](#延伸閱讀)

---

## 快速開始

```powershell
# 安裝相依套件（只需一次）
uv pip install PySide6

# 啟動 GUI
$env:PYTHONPATH = "D:\45_pyCycle_GUI\upstream\pyCycle;D:\45_pyCycle_GUI\tutorials\simple_turbojet"
python D:\45_pyCycle_GUI\tutorials\simple_turbojet\simple_turbojet.py
```

在 GUI 左側調整設計點輸入，按 **▶ Run**。執行結束後左下方日誌會列出所有寫入
`output/` 的檔案，按 **Open output folder** 可直接打開。

---

## GUI 工作流程詳解

```text
┌──────────────────────────────────────────────────────────────────┐
│ ▶ Run / Reset / Open output folder                              │
│                                                                  │
│ ┌── Design Point Inputs ──┐    ┌── Tab：Summary  ───────────┐   │
│ │  Altitude  : 0 ft       │    │ 輸入、Solver log、         │   │
│ │  Mach      : 1e-6       │    │ 三點 viewer 報告、         │   │
│ │  Fn target : 11800 lbf  │    │ comprehensive summary      │   │
│ │  T4 target : 2370 degR  │    ├── Tab：T-S Diagram ────────┤   │
│ │  Comp PR   : 13.5       │    │ Temperature–Entropy 循環   │   │
│ │  Comp η    : 0.83       │    ├── Tab：P-h Diagram ────────┤   │
│ │  Turb η    : 0.86       │    │ Pressure–Enthalpy 循環     │   │
│ └─────────────────────────┘    ├── Tab：Comparison ─────────┤   │
│                                │ 三點四宮格 bar charts       │   │
│ ┌── Log ─────────────────┐    ├── Tab：Component Maps ─────┤   │
│ │  Run started ...        │   │ 壓縮機 / 渦輪 map PNG       │   │
│ │  Solver done in 4.2 s   │   └─────────────────────────────┘   │
│ │  Artefacts written: 14  │                                     │
│ └─────────────────────────┘                                     │
└──────────────────────────────────────────────────────────────────┘
```

操作順序：
1. 在左側調整七個輸入欄位（詳見後文 [GUI 輸入欄位逐項解釋](#gui-輸入欄位逐項解釋)）。
2. 按 **▶ Run**。按鈕停用、進度條啟動，求解器在背景 thread 跑（GUI 不卡住）。
3. 收斂後：
   - **Summary** Tab：純文字 + viewer 表格
   - **T-S / P-h / Comparison** Tab：可縮放、可儲存的互動式 matplotlib 圖
   - **Component Maps** Tab：載入剛存好的壓縮機 / 渦輪 map PNG
4. 全部檔案寫入 `output/`。**Open output folder** 用系統檔案總管打開。

---

## 渦輪噴射熱力學速覽

渦輪噴射的理想熱力循環是 **布雷頓循環（Brayton Cycle）**：

```
1 → 2  Isentropic compression  等熵壓縮       （inlet + compressor）
2 → 3  Isobaric heat addition  等壓加熱       （combustor）
3 → 4  Isentropic expansion    等熵膨脹       （turbine）
4 → 5  Acceleration to exhaust 等熵加速       （nozzle）
5 → 0  Isobaric heat rejection 等壓散熱回大氣 （environment）
```

### 為什麼軸功率要平衡？

渦輪做功 = 壓縮機消耗 + 配件功（本模型忽略配件）。本模型用
`BalanceComp` 解 `turb_PR`，讓 `shaft.pwr_net = 0`。

### 為什麼需要 Newton solver？

三個未知數彼此耦合：

| 未知數 | 由誰決定 | 約束 |
|---|---|---|
| `W` (lbm/s) | 進氣質量流 | 對應淨推力 = Fn target |
| `FAR` | 油氣比 | 對應燃燒室出口溫度 = T4 target |
| `turb_PR` | 渦輪壓比 | 對應軸功率 = 0 |

任何一個改變，另外兩個都會跟著動 → 必須迭代求解。
這就是 `n2.html` 上「上三角」紅色塊的物理本質。

---

## 流動站位與物理意義

本模型沿用 **SAE ARP755** 單軸渦噴站位編號：

```
Ambient    Inlet      Compressor   Combustor    Turbine    Nozzle
   0  ───▶   1   ───▶   2   ───▶    3    ───▶    4   ───▶   5
```

| 站位 | pyCycle 路徑 | 元件 | 物理意義 | 設計點典型值 |
|---|---|---|---|---|
| 0 | `fc.Fl_O` | FlightConditions | 大氣 / 自由流（隨 alt 而變） | Pt=14.7 psia, Tt=518.7 degR |
| 1 | `inlet.Fl_O` | Inlet | 進氣道出口；含 ram recovery | 靜地時 Pt ≈ 14.7 psia |
| 2 | `comp.Fl_O` | Compressor | 壓縮機出口；Pt 大幅上升 | Pt ≈ 200 psia, Tt ≈ 1200 degR |
| 3 | `burner.Fl_O` | Combustor | 燃燒室出口；T = T4 上限 | Tt ≈ 2370 degR, Pt ≈ 195 psia |
| 4 | `turb.Fl_O` | Turbine | 渦輪出口；Pt 下降驅動壓縮機 | Tt ≈ 1810 degR, Pt ≈ 44 psia |
| 5 | `nozz.Fl_O` | Nozzle | 噴嘴出口；Ps 匹配大氣 | Ps ≈ 14.7 psia, V 大幅提高 |

### 從 T-S 圖讀什麼

- **斜率（dT/dS）**：壓縮機與渦輪都應接近等熵（垂直線），若實際 S 增加多，代表效率不足。
- **T 最大值**：燃燒室出口（站 3），亦即 T4，材料極限的觀察點。
- **0–1 距離**：SLS 時近乎重疊；高 Mach 飛行會看到 ram heating 把 1 拉到 0 的右上。

### 從 P-h 圖讀什麼

- **2–3 水平**：等壓加熱（理論上水平，本模型扣 3% 壓損所以 3 略低於 2）。
- **3–4 大斜降**：渦輪膨脹做功。
- **4–5 水平降**：噴嘴。
- **log-y 軸**：壓力跨幾個數量級，log 比 linear 好看清楚高低端細節。

---

## GUI 輸入欄位逐項解釋

左側面板 **Design Point Inputs / 設計點輸入** 共 7 個欄位：

### Altitude / 高度

- **變數路徑**：`DESIGN.fc.alt`
- **單位**：ft
- **預設**：0（海平面）
- **意義**：飛行高度。每升 1000 ft，大氣 P 約降 3.5%、T 約降 1.98 degR。
- **建議調整範圍**：0 ~ 50000 ft（民航上限）。

### Mach / 馬赫數

- **變數路徑**：`DESIGN.fc.MN`
- **單位**：無因次
- **預設**：1×10⁻⁶（近似靜地）
- **意義**：流速 / 當地音速。
- **典型工況**：
  - SLS（設計點）：≈ 0
  - 起飛滾行：0.1–0.25
  - 巡航：0.2–0.85
  - 攔截戰機：1.5–2.5
- **注意**：完全 0 會導致部分數值奇異，使用 `1e-6` 是 pyCycle 的慣例。

### Target Fn / 目標淨推力

- **變數路徑**：`DESIGN.balance.Fn_target`
- **單位**：lbf
- **預設**：11800
- **意義**：設計點要達到的淨推力。Newton solver 會調整空氣質量流量 `W` 來達成此目標。
- **參考量級**：
  - 小型公務機：~1000 lbf
  - 中型支線：~10000 lbf（本模型量級）
  - 雙引擎民航主力：~30000 lbf
  - 軍機後燃加力：~30000 lbf+

### T4 target / 渦輪入口總溫

- **變數路徑**：`DESIGN.balance.T4_target`
- **單位**：degR
- **預設**：2370 degR（≈ 1316 K ≈ 1043 °C）
- **意義**：燃燒室出口、渦輪入口的總溫，是材料負擔最關鍵指標。
- **典型量級**：
  - 民航：1450–1550 K
  - 軍機：1700–1900 K
  - 先進高熱效率：2000 K+（需單晶葉片＋film cooling）
- **⚠ 注意**：T4 是材料極限，過高引擎短壽。本模型 2370 degR 是渦輪入口教學典型值。

### Compressor PR / 壓縮機壓比

- **變數路徑**：`DESIGN.comp.PR`
- **單位**：無因次
- **預設**：13.5
- **意義**：壓縮機把進氣壓力提高的倍數。
- **典型量級**：
  - 早期渦噴 J57：12
  - 本模型範例：13.5（教學中等）
  - 現代高 BPR 渦扇 OPR：40–50（多段壓縮串聯）
- **與 OPR 的關係**：本模型 OPR ≈ comp.PR × inlet recovery（靜地 ≈ 13.5）。

### Compressor η / 壓縮機效率

- **變數路徑**：`DESIGN.comp.eff`
- **單位**：無因次（0–1）
- **預設**：0.83
- **意義**：等熵效率 = 理想做功 / 實際做功。
- **典型量級**：
  - 1950 年代：0.78–0.82
  - 現代軸流壓縮機：0.86–0.92
  - 離心式壓縮機：略低 0.80–0.85

### Turbine η / 渦輪效率

- **變數路徑**：`DESIGN.turb.eff`
- **單位**：無因次（0–1）
- **預設**：0.86
- **意義**：等熵效率 = 實際做功 / 理想做功（注意分子分母與壓縮機相反）。
- **典型量級**：現代渦輪 0.86–0.92。

### 離設計點 OD0 / OD1（程式內固定）

| 工作點 | alt (ft) | MN | Fn target (lbf) | 對應實機情境 |
|---|---:|---:|---:|---|
| OD0 | 0 | 1×10⁻⁶ | 11000 | 地停（比設計點略低油門） |
| OD1 | 5000 | 0.2 | 8000 | 低高度巡航 |

如需更改，編輯 `simple_turbojet.py` 中 `MPTurbojet.setup()` 的
`self.od_pts / self.od_MNs / self.od_alts / self.od_Fns` 列表。

---

## `output/` 完整內容速查

| 檔案 | 內容 | 主要用途 |
|---|---|---|
| `simple_turbojet_summary.txt` / `.pdf` | 輸入清單、求解 log、三點 `viewer` 報告、`comprehensive_performance_summary` | 報告、課堂講義 |
| `simple_turbojet_ts_diagram.png` / `.pdf` | T-S（溫度-熵）循環圖，含 leader line 標籤 | 熱力學課堂、循環分析 |
| `simple_turbojet_ph_diagram.png` / `.pdf` | P-h（壓力-焓）循環圖，log-y 軸 | 元件功量視覺化 |
| `simple_turbojet_comparison.png` / `.pdf` | 設計點 vs OD0 vs OD1 ─ T-S、Fn、TSFC、OPR 四宮格 | 離設計點性能比較 |
| `simple_turbojet_compressor_map_DESIGN_0.png` / `.pdf` | 壓縮機特性圖（含工作點） | Surge margin 評估 |
| `simple_turbojet_turbine_map_DESIGN_0.png` / `.pdf` | 渦輪特性圖（含工作點） | Choke / 效率島評估 |
| `DESIGN.comp.pdf` / `DESIGN.turb.pdf` | pyCycle 內部產生的元件摘要 | 學生作業參考 |
| **`inputs.html`** | OpenMDAO 全輸入變數互動式表格 | 本文件 §7 |
| **`n2.html`** | OpenMDAO N² 互動式系統結構圖 | 本文件 §8 |

> 全部檔案每次按 Run 都會覆寫。若要保留歷史，先手動把 `output/` 改名為
> `output_YYYYMMDD_HHMM/` 再跑。

---

## `inputs.html` 完整解讀

### 1. 它在回答什麼？

> **「這次模擬有哪些輸入？由誰驅動？預設值是什麼？」**

### 2. 表格欄位

| 欄位 | 中文 | 說明 |
|---|---|---|
| `name` / `varname` | 變數名稱 | 完整路徑，如 `DESIGN.balance.Fn_target` |
| `units` | 單位 | OpenMDAO 字串：`lbf`、`degR`、`lbm/s`… |
| `val` | 當下數值 | 通常是 1 元素 numpy array |
| `source` | 來源 | 驅動這個輸入的 *輸出* 路徑；`_auto_ivc.*` = 未連線輸入 = 使用者可改 |
| `prom_name` | 提升名稱 | 對外簡名，如 `Nmech` |
| `min` / `max` | 上下限 | BalanceComp 解出變數常設此限制 |

### 3. 必看區段：`DESIGN.balance.*`

過濾 `DESIGN.balance`，會看到：

```text
DESIGN.balance.Fn_target    val=[11800.0]   units=lbf     source=_auto_ivc.v0
DESIGN.balance.T4_target    val=[2370.0]    units=degR    source=_auto_ivc.v1
DESIGN.balance.lhs:W        val=[…]         units=lbf     source=DESIGN.perf.Fn
DESIGN.balance.lhs:FAR      val=[…]         units=degR    source=DESIGN.burner.Fl_O:tot:T
DESIGN.balance.lhs:turb_PR  val=[…]         units=hp      source=DESIGN.shaft.pwr_net
```

這幾行直接表達 Newton solver 要解的三條方程式：

| 平衡變數 | LHS | = | RHS |
|---|---|---|---|
| `W` | `perf.Fn` 實際淨推力 | = | `Fn_target = 11800 lbf` |
| `FAR` | `burner.Fl_O:tot:T` 燃燒室出口溫度 | = | `T4_target = 2370 degR` |
| `turb_PR` | `shaft.pwr_net` 軸功率 | = | `0` |

### 4. 三大實際工程應用

#### 例 1：抓單位錯置（lbf vs N）

新人把 `Fn_target` 填成 `52500`（誤以為單位是 N）。在 `inputs.html` 過濾
`Fn_target` 立刻看到 `units=lbf, val=[52500]` = 52500 lbf ≈ 233 kN，
明顯超出本模型量級，可在 Newton 跑爆前抓到。

#### 例 2：「設計變數」= 全部 `_auto_ivc`

對 `source` 欄篩 `_auto_ivc`，得到本次模擬完整的 input deck：

- `DESIGN.fc.alt / fc.MN`
- `DESIGN.comp.PR / comp.eff / turb.eff`
- `DESIGN.balance.Fn_target / T4_target`
- `OD0.fc.alt / OD0.fc.MN / OD0.balance.Fn_target`
- `OD1.fc.alt / OD1.fc.MN / OD1.balance.Fn_target`

把這份清單貼進報告就是「本次模擬輸入全表」，無遺漏。

#### 例 3：對比 DESIGN vs OD 的 `Nmech` 處理

```text
DESIGN.Nmech    source=_auto_ivc.*        ← 設計點固定 8070 rpm
OD0.Nmech       source=OD0.balance.Nmech  ← OD 由 balance 解出
OD1.Nmech       source=OD1.balance.Nmech
```

→ 不看程式碼也能讀出架構決策：設計時固定轉速、OD 時轉速由平衡解出。

---

## `n2.html` 完整解讀

### 1. 它在回答什麼？

> **「模型內部資料怎麼流？哪裡有回授？Newton solver 在解什麼？」**

### 2. 介面與操作

- **對角線**：依執行順序排列的元件（灰色方塊）。
- **下三角**：前饋連線 — 上游 → 下游，自然執行可解。
- **上三角**：**回授連線** — 必須 Newton solver 才能解。
- **左側樹**：可展開的階層 DESIGN / OD0 / OD1 → 各自的 fc / inlet / comp / …
- **頂部 Search**：高亮特定變數的所有連線。
- **點對角元件**：展開內部子結構。

### 3. 本模型的關鍵連線

**下三角（前饋，藍/橘色）**：

```
fc.Fl_O ─▶ inlet.Fl_I
inlet.Fl_O ─▶ comp.Fl_I
comp.Fl_O ─▶ burner.Fl_I
burner.Fl_O ─▶ turb.Fl_I
turb.Fl_O ─▶ nozz.Fl_I
comp.trq ─▶ shaft.trq_0
turb.trq ─▶ shaft.trq_1
perf.Fn ─▶ balance.lhs:W
burner.Fl_O:tot:T ─▶ balance.lhs:FAR
shaft.pwr_net ─▶ balance.lhs:turb_PR
```

**上三角（回授，紅色）— Newton solver 戰場**：

```
balance.W ─▶ inlet.Fl_I:stat:W       ← 解出的 W 餵回入口
balance.FAR ─▶ burner.Fl_I:FAR       ← 解出的 FAR 餵回燃燒室
balance.turb_PR ─▶ turb.PR           ← 解出的 turb_PR 餵回渦輪
```

→ **看到三條上三角連線就知道 Newton 在解 3 維方程式**。

### 4. DESIGN ↔ OD 連線

```
DESIGN.<comp>.s_PR / s_Wc / s_eff / s_Nc   ─▶  OD*.<comp>.s_*
DESIGN.nozz.Throat:stat:area               ─▶  OD*.balance.rhs:W
```

→ 「設計尺寸鎖定後，OD 不能改尺寸、只能改操作點」這個工程慣例在 N² 圖上完全視覺化。

### 5. 四大實際工程應用

#### 例 1：debug 不收斂

Newton 在第 15 次 NaN。打開 N² 搜 `Wfuel`，發現 `burner.Wfuel → perf.Wfuel_0` 沒
接到 → TSFC 計算永遠 0 → balance 永遠差很多。N² 圖上該格 *沒有顏色塊*，幾秒
抓出問題。

#### 例 2：跨組溝通架構

向結構組同事解釋雙轉子為何要兩組 BalanceComp，用 N² 比口頭快 10×：
「你看上三角這兩塊：HP shaft 平衡、LP shaft 平衡，獨立。中間紅色說明 LP 渦輪
功率回 fan，不能拆解先後執行。」

#### 例 3：Newton 維度最小化

某 cycle 上三角 7 個回授（Newton 解 7 維）→ 用 `solve_subsystems=True` 把兩條
inlet ↔ comp 熱平衡推到內層解 → 外層 Newton 降到 5 維 → 求解時間 −35%。

#### 例 4：認證審查

FAA / EASA 引擎模型有 traceability 要求。N² 圖（PDF 列印版）通常貼進
Engine Model Description Document，作為「架構正確性」客觀證據。

---

## 工程實務應用情境

### 情境 A：起飛推力規格驗證

> **需求**：客戶要 11800 lbf SLS，T4 不超過 2370 degR。

1. GUI：`alt=0, MN=1e-6, fn=11800, T4=2370, PR=13.5, η_c=0.83, η_t=0.86`
2. 跑完看 `simple_turbojet_summary.txt`，確認 DESIGN 點 Fn ≈ 11799.998 lbf。
3. 過 `inputs.html` 確認沒有遺漏輸入。
4. 截圖 `n2.html` 的 DESIGN 子區塊附在交付文件。

### 情境 B：巡航油耗評估

> **需求**：客戶問「5000 ft、Mach 0.2、8000 lbf 推力時 TSFC？」

1. OD1 已在程式內預設此條件，直接跑 GUI。
2. `simple_turbojet_comparison.png` 右下 TSFC 柱即答案。
3. 過 `inputs.html` OD1 區塊確認 `fc.alt=5000, fc.MN=0.2, balance.Fn_target=8000`。

### 情境 C：壓縮機選型比較

> **需求**：兩款候選壓縮機（PR=13.5，η 略異）評估 surge margin。

1. 跑兩次 GUI，每次先把 `output/` 改名保留歷史。
2. 對比 `simple_turbojet_compressor_map_DESIGN_0.png` 工作點與 surge line 距離。
3. 過 `n2.html` 確認兩次跑都使用相同的 `comp.s_*` 連線（排除架構差異干擾）。

### 情境 D：冷天 / 熱天靈敏度

> **需求**：機場熱浪 +25°C，看是否仍能達到 SLS 推力。

本模型未直接暴露 `dT_amb`，可在 `MPTurbojet.setup` 加上 `set_input_defaults`：

```python
self.set_input_defaults('DESIGN.fc.dTs', val=25.0, units='degR')
```

> 冷天 Tt 降低 → 密度上升 → 同 W 對應更大壓縮功 → Fn 升高，TSFC 改善；熱天相反。
> 民航起飛 limit weight 最大的影響因子。

### 情境 E：教學課堂

- 投影 `n2.html`，現場展開 DESIGN ↔ OD1 比較 balance 連線差異。
- 讓學生過 `inputs.html` 找出「全部未連線輸入」並分類為「飛行條件」、「元件特性」、「性能目標」。
- T-S / P-h 圖 + summary 是標準的循環分析作業。

---

## 收斂與環境問題排除

### Newton 不收斂

**症狀**：log 顯示 `NL: Newton FAILED to converge` 或出現
`RuntimeWarning: invalid value encountered in sqrt` 後 NaN。

**檢查順序**：

1. `n2.html` 上三角是否有預期外連線？多餘回授會增加 Newton 維度。
2. `inputs.html` 過濾 `balance`，確認 LHS / RHS 物理量級與單位都對。
3. 初始猜值 `prob['DESIGN.balance.FAR'] = 0.01755...` 是否偏離太遠？
4. T4 是否高到燃燒室不可能達到（或低到 FAR 變負）？
5. 試把 `newton.options['maxiter']` 從 15 加到 30。

### PySide6 報錯 `ModuleNotFoundError`

```powershell
uv pip install PySide6
```

### 圖表中文亂碼

GUI 嘗試字體序列：`Microsoft YaHei → SimHei → Arial Unicode MS → DejaVu Sans`。
亂碼時：

```powershell
# 安裝 Noto Sans TC
choco install noto -y    # 或從 Google Fonts 下載 .ttf 手動安裝
```

並在 `simple_turbojet.py` 開頭加入新字體名到
`matplotlib.rcParams['font.sans-serif']` 列表。

### `output/` 沒出現

v0.2.0 起所有輸出集中在 `tutorials/simple_turbojet/output/`。如果在 repo 根目錄
看到舊的 `simple_turbojet_out/`，那是早期版本殘留，可手動刪除。

### OpenMDAO `set_reports_dir has been removed`

OpenMDAO 3.40 移除該函式。本模組改採 `os.chdir(OUT_DIR)` +
`_flatten_openmdao_reports()`。如未來 3.41+ 提供官方 redirect API，可換用。

### `n2.html` 打不開或卡頓

檔案 ~1 MB 含 JS。建議用 Chrome / Edge / Firefox。停用廣告封鎖類擴充。

### 站位標籤又重疊

v0.2.0 用 `STATION_LABEL_OFFSETS` 為每個站位安排固定方向。如果你大幅改 PR、T4
導致兩點極端靠近，可在 `simple_turbojet.py` 內修改該常數的偏移向量。

---

## 常見問題 FAQ

**Q1：每次跑都會覆寫 `output/`，可以保留歷史嗎？**
A：手動 `Rename-Item output output_20260512_1430`，再按 Run。

**Q2：可以改成只跑設計點，不算 OD0 / OD1 嗎？**
A：可以。在 `MPTurbojet.setup` 把 `self.od_pts = []`，並把對應的 `pyc_use_default_des_od_conns` 注釋掉。

**Q3：GUI 中文字斷字奇怪？**
A：Qt 預設字體在繁中環境可能渲染怪。在 Windows 確認 `font.sans-serif` 序列裡有
`Microsoft JhengHei UI`。或安裝 `Noto Sans TC` 並把它列在最前。

**Q4：可以加更多 OD 點嗎？例如 4 個離設計點？**
A：在 `MPTurbojet.setup` 加入 `self.od_pts = ['OD0','OD1','OD2','OD3']` 與對應
`od_MNs / od_alts / od_Fns`，初始猜值的 for-loop 會自動跑。注意 GUI 端的
comparison 圖只取 `colors[:N]`，超過 5 點需自訂 colors 列表。

**Q5：能輸出 SI 單位（kN, K, kPa）嗎？**
A：pyCycle 使用 OpenMDAO 的 units 系統，輸入端可以指定 SI 單位（如
`prob.set_val('...', val=52.5, units='kN')`），但內建 map 與 viewer 的格式仍以
美制顯示。要完全 SI 顯示需要重寫 viewer / `comprehensive_performance_summary`。

**Q6：N² 想印成 PDF？**
A：在瀏覽器先 *Expand All*，然後 *Print → Save as PDF*，紙張選 A3 橫向比較不擠。

**Q7：要把這套模組嵌進更大的 OpenMDAO 模型可以嗎？**
A：可以。`Turbojet` 與 `MPTurbojet` 是純 pyCycle 類別，可在其他 OpenMDAO 模型中
用 `self.add_subsystem('engine', MPTurbojet())` 嵌入。GUI 部分（`launch_gui`、
`CycleWorker` 等）只在 `__main__` 觸發，不影響嵌入。

**Q8：執行很久，是不是卡住？**
A：第一次 import pyCycle + OpenMDAO 約需 5–10 秒；solver 本身約 3–8 秒（依機器）。
合計 8–18 秒屬正常。若超過 60 秒一直跑，可能 Newton 卡死，請看左下日誌或在
PowerShell 看 stderr。

---

## 延伸閱讀

### 本模組相關

- `simple_turbojet.py` 原始碼：所有元件接線、GUI 邏輯、輸出搬移邏輯都在這一個檔。
- [`reference.html`](./reference.html)：本目錄附的離線中英對照手冊（縮寫、元件、檔案、實例）。
- `upstream/pyCycle/example_cycles/simple_turbojet.py`：上游官方範例（**唯讀**）。

### OpenMDAO

- N² Diagram、Reports System、BalanceComp、`get_outputs_dir()`、`get_reports_dir()`。
- 設定 Newton solver options：`atol`、`rtol`、`maxiter`、`solve_subsystems`。

### 熱力學教材

- Mattingly, *Elements of Propulsion: Gas Turbines and Rockets*
- Hill & Peterson, *Mechanics and Thermodynamics of Propulsion*
- Cumpsty, *Jet Propulsion*

### 站位編號規範

- SAE ARP755D — *Aircraft Propulsion System Performance Station Designation*
- NASA Glenn 線上教材（Brayton cycle、turbojet thrust equation）

---

## 變更摘要

| 版本 | 日期 | 重要變更 |
|---|---|---|
| 0.2.0 | 2026-05-12 | 初版發布；GUI + bilingual user guide + `reference.html` |

完整變更紀錄請見專案根目錄的 `CHANGELOG.md`。
