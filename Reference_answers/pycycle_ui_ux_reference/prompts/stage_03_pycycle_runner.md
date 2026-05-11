# Stage 03 Prompt: Connect pyCycle Runner

## 給 AI 的提示詞

```text
請開始把 PySide6 UI 連接到 pyCycle。
限制：
1. upstream/pyCycle 只能唯讀參考，不可修改。
2. 優先複用 upstream/pyCycle/example_cycles/high_bypass_turbofan.py 的概念。
3. 在 src/pycycle_edu_ui/runner/ 建立 wrapper，不要把 upstream 範例直接改掉。
4. wrapper 可以 import upstream 的 MPhbtf 與 viewer，但只跑 DESIGN 與一個 OD 點，不要直接跑完整大掃描。
5. runner 執行後必須保存 pyCycle 原始英文 hbtf_view.out。
6. runner 要解析淨推力、TSFC、OPR、BPR、Mach、高度、gross thrust 與 ram drag。
7. UI 要把解析結果和 CFM56-7B 公開資料放進表格與圖表。
8. 正體中文報告要由 app 產生，並標明英文 viewer 路徑、來源與模型限制。
9. pyCycle 計算要放在背景 thread，避免 UI 在求解期間停止回應。
10. 請先建立最小可測試版本，並補上驗證命令。
```

## 預期結果

- UI 可以呼叫 pyCycle wrapper 並顯示真實 pyCycle 計算結果。
- app 同時保存 pyCycle 英文 viewer 與正體中文比對報告。
- 報告明確標示「公開資料」、「pyCycle 範例」、「假設條件」與「模型限制」。
