# Source Manifest: CFM56-7B / pyCycle 教學驗證

存取日期：2026-05-11  
用途：支援「AI 提示詞、uv、pyCycle、PySide6 UI」教學 PPT，並作為後續 CFM56-7B 高旁通比渦扇模型驗證來源。

## 已存入本資料夾的檔案

| 檔案 | 類型 | 用途 |
|---|---|---|
| `nasa-20170000232-pycycle-openmdao.pdf` | NASA PDF | pyCycle / OpenMDAO 相關方法背景與循環分析教學來源。 |
| `openmdao-pycycle-readme.md` | 上游 README | pyCycle 安裝、版本相容性、範例與引用資訊。 |
| `aircraft-commerce-cfm56-7b-specs.pdf` | CFM56-7B 規格整理 PDF | 教學用 CFM56-7B 公開規格交叉檢查來源。 |

## 官方與可信來源 URL

| 來源 | URL | 狀態 | 可用欄位 |
|---|---|---|---|
| CFM International CFM56-5B / CFM56-7B | https://www.cfmaeroengines.com/cfm56/CFM56-5B-CFM56-7B | 命令列下載遇到 Vercel security checkpoint；保留 URL 與搜尋結果佐證 | CFM56-7B 系列、推力級距、應用機型、原廠背景 |
| CFM International CFM56 brochure PDF | https://www.cfmaeroengines.com/wp-content/uploads/2017/09/Brochure_CFM56_fiches_2017.pdf | 命令列下載遇到 Vercel security checkpoint；保留 URL | CFM56 系列規格、推力、旁通比、壓比、尺寸 |
| Safran CFM56 overview | https://www.safran-group.com/products-services/cfm56-best-selling-engine-commercial-aviation-history | 命令列下載遇到 Cloudflare block；保留 URL | CFM56 商用航空背景、銷售/服役脈絡 |
| OpenMDAO pyCycle GitHub README | https://github.com/OpenMDAO/pyCycle | 已存 raw README | 安裝方式、OpenMDAO 版本相容性、範例建議、引用格式 |
| pyCycle paper, Aerospace 2019 | https://www.mdpi.com/2226-4310/6/8/87 | PDF 命令列下載遇到 access denied；上游 README 提供 DOI 與 citation | pyCycle 方法、OpenMDAO/NPSS 脈絡、設計/非設計點分析 |

## 第一版驗證目標

選用 CFM56-7B 作為教學案例，理由如下：

- 主流商用高旁通比渦扇，資料多且學生容易查證。
- 應用於 Boeing 737NG，教學情境具體。
- pyCycle 內建 `upstream/pyCycle/example_cycles/high_bypass_turbofan.py`，可作為高旁通比雙轉軸渦扇範例骨架。
- 範例中的設計旁通比約 `5.105`，適合作為 CFM56-7B 等級發動機的初階比較起點，但不應宣稱等同真實 CFM56-7B engine deck。

## 建議後續擷取欄位

- Engine family / variant
- Application aircraft
- Sea-level static thrust
- Bypass ratio
- Overall pressure ratio
- Fan diameter
- Length / dry weight
- Fuel type
- Validation notes: 哪些欄位可直接對照 pyCycle，哪些只能作為工程合理性檢查

