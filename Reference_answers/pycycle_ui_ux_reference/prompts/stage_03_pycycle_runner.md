# Stage 03 Prompt: Connect pyCycle Runner

## 給 AI 的提示詞

```text
請開始把 PySide6 UI 連接到 pyCycle。
限制：
1. upstream/pyCycle 只能唯讀參考，不可修改。
2. 優先複用 upstream/pyCycle/example_cycles/high_bypass_turbofan.py 的概念。
3. 在 src/pycycle_edu_ui/runner/ 建立 wrapper，不要把 upstream 範例直接改掉。
4. UI 輸入的 BPR、OPR、Tt4、高度、馬赫數要可以傳給 runner。
5. runner 執行後回傳淨推力、TSFC、站點總溫/總壓、燃油流量與效率資料。
6. 所有資料來源與模型限制要能寫進正體中文與英文報告。
7. 請先建立最小可測試版本，並補上驗證命令。
```

## 預期結果

- UI 不再只顯示教學估算，而是可以呼叫 pyCycle wrapper。
- 報告明確標示「公開資料」、「pyCycle 範例」、「假設條件」與「模型限制」。
