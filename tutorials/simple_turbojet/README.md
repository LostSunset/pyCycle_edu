# Simple Turbojet 教學說明

本目錄是 pyCycle 簡易渦輪噴射引擎（single-spool turbojet）的互動教學。執行 `simple_turbojet.py` 會開啟 PySide6 圖形介面，輸入設計點參數（高度、馬赫數、目標推力等），即可計算設計點與兩個離設計點（off-design）的循環，並把所有結果寫到 `output/` 子資料夾。

本文件聚焦於 **如何讀懂 OpenMDAO 自動產生的 `inputs.html` 與 `n2.html`**，並用實機工程情境舉例。

---

## 目錄

1. [快速開始](#快速開始)
2. [output/ 內容速查](#output-內容速查)
3. [inputs.html 完整解讀](#inputshtml-完整解讀)
4. [n2.html 完整解讀](#n2html-完整解讀)
5. [工程實務應用情境](#工程實務應用情境)
6. [常見問題](#常見問題)

---

## 快速開始

```powershell
# 安裝相依套件（只需一次）
uv pip install PySide6

# 啟動 GUI
$env:PYTHONPATH = "D:\45_pyCycle_GUI\upstream\pyCycle;D:\45_pyCycle_GUI\tutorials\simple_turbojet"
python D:\45_pyCycle_GUI\tutorials\simple_turbojet\simple_turbojet.py
```

在 GUI 左側調整設計點輸入，按 **▶ Run**。執行結束後左下方日誌會列出所有寫入 `output/` 的檔案，按 **Open output folder** 可直接打開。

---

## `output/` 內容速查

| 檔案 | 內容 | 主要用途 |
|---|---|---|
| `simple_turbojet_summary.txt` / `.pdf` | 文字摘要：輸入、求解 log、各工作點性能、流動站、元件效率 | 報告、課堂講義 |
| `simple_turbojet_ts_diagram.png` / `.pdf` | T-S（溫度-熵）循環圖 | 熱力學課堂、循環分析 |
| `simple_turbojet_ph_diagram.png` / `.pdf` | P-h（壓力-焓）循環圖 | 元件功量視覺化 |
| `simple_turbojet_comparison.png` / `.pdf` | 設計點 vs OD0/OD1：T-S、推力、TSFC、OPR 四宮格 | 離設計點比較 |
| `simple_turbojet_compressor_map_DESIGN_0.*` | 壓縮機特性圖（含工作點） | Surge margin 評估 |
| `simple_turbojet_turbine_map_DESIGN_0.*` | 渦輪特性圖（含工作點） | Choke 評估 |
| `DESIGN.comp.pdf` / `DESIGN.turb.pdf` | pyCycle 內部產生的元件圖 | 同上 |
| **`inputs.html`** | OpenMDAO 自動產生的輸入變數清單 | **本文件主題之一** |
| **`n2.html`** | OpenMDAO N² (N-squared) 互動式系統結構圖 | **本文件主題之一** |

---

## `inputs.html` 完整解讀

### 1. 這是什麼

`inputs.html` 是 OpenMDAO 自動掃描整個 `Problem` 後，把 **所有輸入變數** 列成一張可篩選的表格。每一個輸入都會被它的某一個來源驅動：

- 來自其它元件的輸出 → 在表格的 *Source* 欄會看到完整路徑（例如 `DESIGN.fc.Fl_O:stat:P`）。
- 沒有被連線的「未連線輸入」（unconnected） → 由 `set_input_defaults`、`set_val`、或 `IndepVarComp` 提供初始值。

> 在 pyCycle 教學情境，**未連線輸入** 就是使用者真正會調整的設計變數；**已連線輸入** 則代表循環內部的物理連結（流動接續、扭矩平衡等）。

### 2. 介面欄位

開啟 `output/inputs.html`，可以看到一張表格，常見欄位：

| 欄位 | 意義 |
|---|---|
| `name` 或 `varname` | 完整變數路徑，例如 `DESIGN.comp.Fl_I:stat:W` |
| `units` | 單位字串，如 `lbm/s`、`degR`、`lbf` |
| `val` | 當下數值（陣列） |
| `source` | 驅動這個輸入的輸出來源；未連線者顯示為 `_auto_ivc.<name>` |
| `prom_name` | 提升後的對外名稱（如 `Nmech`） |
| `min` / `max` | 上下限（若設定） |

上方通常有篩選列：輸入「balance」就能快速看所有 BalanceComp 的相關欄位；輸入 `Fl_I` 可以看到所有流動接口。

### 3. 用 `simple_turbojet` 來具體舉例

執行 GUI 後在 `inputs.html` 用過濾欄輸入 `DESIGN.balance`，會看到：

```
DESIGN.balance.Fn_target    val=[11800.0]   units=lbf    source=_auto_ivc.v0
DESIGN.balance.T4_target    val=[2370.0]    units=degR   source=_auto_ivc.v1
DESIGN.balance.lhs:W        val=[...]       units=lbf    source=DESIGN.perf.Fn
DESIGN.balance.rhs:W        ...             ...          source=_auto_ivc...
DESIGN.balance.lhs:FAR      val=[...]       units=degR   source=DESIGN.burner.Fl_O:tot:T
DESIGN.balance.lhs:turb_PR  val=[...]       units=hp     source=DESIGN.shaft.pwr_net
```

從這幾行可以**一眼看出 Newton solver 要解的三條方程式**：

| 平衡變數 | LHS（左式） | = | RHS（右式） |
|---|---|---|---|
| `W` (空氣質量流量) | `perf.Fn`（實際淨推力 lbf） | = | `Fn_target = 11800 lbf` |
| `FAR` (油氣比) | `burner.Fl_O:tot:T`（燃燒室出口溫度 degR） | = | `T4_target = 2370 degR` |
| `turb_PR` (渦輪壓比) | `shaft.pwr_net`（軸淨功率 hp） | = | `0`（功率平衡） |

也就是：**Newton 求解器要找一組 (W, FAR, turb_PR)，讓引擎在 11800 lbf 淨推力、2370 degR 渦輪入口溫度、且壓縮機與渦輪功率平衡**。

### 4. 真實工程應用

**例 1：單位錯置抓蟲（最常見的低階致命錯）**

某次新人接手 cycle deck，把 `Fn_target` 寫成 `52500`（誤以為單位是 N），但 `units='lbf'`。後果：等於要求 52500 lbf ≈ 233 kN 的推力，遠超出設計，Newton 不收斂。
打開 `inputs.html` 過濾 `Fn_target` 一眼就看到 `units=lbf, val=[52500]`，與引擎尺寸不合，立刻發現單位混淆。

**例 2：未連線輸入清單 = 設計變數清單**

對 `source` 欄做 `_auto_ivc` 篩選，會列出所有沒被內部連線的輸入。對本模型來說，就是：

- `DESIGN.fc.alt`、`DESIGN.fc.MN`（飛行條件）
- `DESIGN.comp.PR`、`DESIGN.comp.eff`、`DESIGN.turb.eff`（設計目標）
- `DESIGN.balance.Fn_target`、`DESIGN.balance.T4_target`（性能目標）
- `OD0.fc.alt`、`OD0.fc.MN`、`OD0.balance.Fn_target`（OD0 工作點）
- `OD1.fc.alt`、`OD1.fc.MN`、`OD1.balance.Fn_target`（OD1 工作點）

→ 任何一份正式的設計報告，把這份清單貼上去就是「本次模擬的 input deck 全表」，無遺漏。

**例 3：核對 `set_input_defaults`**

教科書熱循環假設 `Nmech` 是設計參數，但本模型把它列為 `set_input_defaults('DESIGN.Nmech', 8070, 'rpm')`，是預設值而非平衡變數。
透過 `inputs.html` 過濾 `Nmech`：

```
DESIGN.Nmech    val=[8070.0]   units=rpm    source=_auto_ivc.<...>
OD0.Nmech       val=[...]      units=rpm    source=OD0.balance.Nmech   ← OD 工作點被 balance 驅動！
OD1.Nmech       val=[...]      units=rpm    source=OD1.balance.Nmech
```

可清楚對比：**設計點是「固定轉速」，離設計點則由 balance 解出轉速**。沒看程式碼也能讀懂這個架構決策。

---

## `n2.html` 完整解讀

### 1. 這是什麼

N² (N-squared) 圖是航太/系統工程界的標準視覺化工具：
- **對角線（diagonal）**：每個元件依執行順序排成一列。
- **下三角（below diagonal）**：表示 *前饋（feed-forward）* 連線 —— 上游元件的輸出送到下游元件的輸入，自然執行順序即可解出。
- **上三角（above diagonal）**：表示 *回授（feedback）* 連線 —— 下游元件的輸出回到上游輸入。這代表 **必須用迭代求解器（Newton/Krylov）** 才能解出。

OpenMDAO 把 N² 矩陣做成 *互動式 HTML*：可以縮放、點擊展開/收合子系統、滑鼠停在格子上看連線資訊、用 *Find* 高亮特定變數的路徑。

### 2. 操作要點

打開 `output/n2.html`：

- **左側面板**：樹狀導覽，列出 `DESIGN`、`OD0`、`OD1` 三個 sub-problem；每個下面有 `fc`、`inlet`、`comp`、`burner`、`turb`、`nozz`、`shaft`、`perf`、`balance`。
- **中央主圖**：N² 矩陣本身。對角元件 = 灰色方塊；連線 = 橘/藍色方塊。
- **頂部工具列**：
  - `Collapse All / Expand All`：可逐層展開
  - `Search`：輸入變數名稱，高亮所有相關連線
  - `Solver` 切換：可同時看 *資料連線* 與 *求解器階層*
- **互動操作**：
  - 點擊對角元件 → 展開該元件的內部子結構
  - 滑鼠停在離對角格子 → 顯示 `output → input` 配對
  - 右鍵 → 把該節點設為根，聚焦觀察

### 3. 從本模型讀出的關鍵結構

#### 3.1 設計點 `DESIGN` 子系統（展開後）

執行順序：`fc → inlet → comp → burner → turb → nozz → shaft → perf → balance`

下三角的「正常」前饋連線：
- `fc.Fl_O:tot:*` → `inlet.Fl_I:tot:*`
- `inlet.Fl_O` → `comp.Fl_I`
- `comp.Fl_O` → `burner.Fl_I`
- `burner.Fl_O` → `turb.Fl_I`
- `turb.Fl_O` → `nozz.Fl_I`
- `comp.trq` → `shaft.trq_0`、`turb.trq` → `shaft.trq_1`
- `perf.Fn`、`burner.Fl_O:tot:T`、`shaft.pwr_net` → `balance.lhs:*`

**上三角（回授）連線 —— 觀察重點**：
- `balance.W` → `inlet.Fl_I:stat:W`：求出的質量流量送回入口
- `balance.FAR` → `burner.Fl_I:FAR`：求出的油氣比送回燃燒室
- `balance.turb_PR` → `turb.PR`：求出的渦輪壓比送回渦輪

→ 看到三條明顯的「上三角」連線，立即知道 **這個循環需要 Newton solver 才能閉迴路收斂**。

#### 3.2 多工作點階層

最外層展開後可看到 `DESIGN`、`OD0`、`OD1` 三個 sub-problem 並列。它們之間以 `pyc_use_default_des_od_conns` 與 `pyc_connect_des_od` 互通：

- `DESIGN.<元件>.s_*`（scalar size factors，如壓縮機 map 縮放係數） → `OD0.<元件>.s_*`、`OD1.<元件>.s_*`
- `DESIGN.nozz.Throat:stat:area` → `OD0.balance.rhs:W`、`OD1.balance.rhs:W`（噴嘴喉部固定）

→ N² 圖中央會看到 *DESIGN 區塊送出的縮放係數，往下傳到 OD 區塊*，這正是「設計尺寸鎖定後，OD 點只能調節操作條件」的架構視覺化。

### 4. 真實工程應用

**例 1：debug 不收斂**

跑了一個自訂的 cycle，Newton 在第 15 次迭代 NaN。打開 N² 圖搜尋 `Wfuel`，發現 `burner.Wfuel → perf.Wfuel_0` 這條連線沒接到，導致 TSFC 計算永遠 0、balance.lhs:FAR 與 RHS 永遠差很多。N² 圖上該位置 *沒有顏色塊*，幾秒就抓出問題（找 source code 要翻很久）。

**例 2：和其他工程師溝通架構**

向結構組同事解釋「為什麼這個雙轉子需要兩組 BalanceComp」時，用 N² 圖比口頭講快十倍：

> 「你看上三角這兩塊：HP shaft 平衡、LP shaft 平衡，各自獨立。中間這塊紅色說明 LP turbine 的功率送回 fan，不能拆解先後執行。」

對於跨領域 review（aero/structures/controls），N² 是 *語意中性* 的共同語言。

**例 3：回授迴路最小化**

某型號 cycle deck 原本上三角有 7 個回授連線（Newton 要解 7 維方程），收斂緩慢。透過 N² 圖檢查發現：兩條來自 inlet ↔ comp 的內部熱平衡其實可以用 `solve_subsystems=True` 在更內層解掉，把外層 Newton 維度降到 5。重構後求解時間下降 35%。

→ N² 圖把 **「Newton 維度」變成可視結構**，是性能調校的入手點。

**例 4：認證審查**

FAA / EASA 對引擎模型有 traceability 要求。N² 圖（PDF 列印版）通常會貼進 *Engine Model Description Document*，作為「架構正確性」的客觀證據。比文字描述更具說服力，也更不易出爭議。

---

## 工程實務應用情境

把 GUI 跟 `inputs.html` / `n2.html` 串成 **完整 design-review 流程**：

### 情境 A：起飛推力規格驗證

> 場景：客戶要求 11800 lbf 海平面靜推力（Sea Level Static, SLS），同時不能超過 T4 = 2370 degR（材料極限）。

1. GUI 中設定 `altitude = 0 ft, mach = 1e-6, fn_target = 11800 lbf, t4_target = 2370 degR`。
2. 跑完看 `simple_turbojet_summary.txt`，確認 SLS 點 Fn 收斂於 11799.9 lbf，TSFC ≈ 0.81。
3. 打開 `inputs.html` 確認沒有遺漏輸入。
4. 打開 `n2.html` 截圖 `DESIGN` 子區塊，附在交付文件。

### 情境 B：巡航油耗評估

> 場景：客戶換問「5000 ft、Mach 0.2、8000 lbf 推力時的 TSFC？」

1. GUI 跑完，OD1 工作點 TSFC 數值已在 `comparison.png` 四宮格條圖右下。
2. 過 `inputs.html` 看 OD1 區塊 → `OD1.fc.alt=5000, OD1.fc.MN=0.2, OD1.balance.Fn_target=8000`，確認沒被誤改。
3. N² 圖檢查 OD1 ↔ DESIGN 的尺寸鎖定連線健在。

### 情境 C：壓縮機選型比較

> 場景：候選兩款壓縮機，BPR 不同但 PR 同為 13.5。要評估 surge margin。

1. 兩種設定各跑一次（修改 `comp.PR` 或 `comp.eff` 或換 `map_data`）。
2. 比較 `simple_turbojet_compressor_map_DESIGN_0.png` 上的工作點與 surge line 距離。
3. N² 圖確認雙方在 `comp.s_*` 縮放係數的連線一致，排除架構差異干擾。

### 情境 D：教學課堂使用

- 一邊跑 GUI，一邊在投影機展示 `n2.html`，當場切換 DESIGN ↔ OD1，讓學生看到「balance 連線在 OD 點重新配置」的差異。
- 拿 `inputs.html` 出考題：「找出本 cycle 全部未連線輸入，並判斷哪些是熱力目標、哪些是元件特性。」
- T-S / P-h 圖搭配文字摘要，整套就是一份標準的循環分析作業。

---

## 常見問題

**Q1：n2.html 開不起來，瀏覽器卡住。**
A：檔案約 1 MB，含內嵌 JavaScript。建議用 Chrome / Edge / Firefox 直接拖檔開啟，不要用 IE/舊 Safari。檔案太大時可在 GUI 開啟前停用瀏覽器擴充。

**Q2：跑完後 `output/` 裡看到舊檔殘留。**
A：本 GUI 每次 Run 都會覆寫同名檔。如需保留歷史，建議手動 rename 整個 `output/` 為 `output_YYYYMMDD/` 後再跑下一次。

**Q3：`inputs.html` 找不到我剛改的參數。**
A：GUI 內的輸入要 *按下 Run* 後才會送到 `prob.set_val`，舊的 `inputs.html` 是上次跑的結果。

**Q4：N² 上某個對角元件展開後是空的。**
A：表示該元件沒有子系統（純 ExplicitComponent）。例如 `balance` 展開後只有它自己內部的方程式，是正常現象。

**Q5：n2.html 想印成 PDF。**
A：在瀏覽器先 *Expand All*，然後 *Print → Save as PDF*，紙張選 A3 橫向比較不會擠。也可直接用 `simple_turbojet_summary.pdf` 內的文字摘要做正式交付。

---

## 延伸閱讀

- `simple_turbojet.py` 內 `Turbojet.setup()` — 元件接線完整原始碼。
- pyCycle 上游：`upstream/pyCycle/example_cycles/simple_turbojet.py` — 原始官方範例。
- OpenMDAO 文件：N² Diagram、Reports System、BalanceComp。
- `simple_turbojet_summary.txt` 中段的 `Comprehensive Performance Analysis` —— 列出所有流動站的溫壓速度、元件效率，可與 N² 圖對讀。
