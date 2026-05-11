# Stage 01 Prompt: UI/UX Template Selection

## 給 AI 的提示詞

```text
請先上網查詢適合 PySide6 工程軟體的 UI/UX 模板或元件庫。
需求：
1. 必須可用於 PySide6。
2. 適合工程分析軟體，不要做成行銷網站或遊戲介面。
3. 要能支援側邊導覽、參數表單、結果卡片、表格、圖表與報告區。
4. 視覺風格請套用 Claude 類型的米色、暖色、細線框、低對比、可閱讀設計。
5. 請列出 2 到 3 個候選方案、優缺點、來源連結，最後推薦一個方案。
6. 推薦後先不要改檔，等我確認。
```

## 參考答案重點

- 推薦 `PySide6 + QFluentWidgets / 自訂 Claude 米色主題 + pyqtgraph`。
- 若學生電腦無法安裝 QFluentWidgets，保留 Qt Widgets fallback。
- 圖表使用 `pyqtgraph`，因為它適合 PySide6 工程與科學互動圖表。
