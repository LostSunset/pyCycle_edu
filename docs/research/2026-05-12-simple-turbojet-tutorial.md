# 2026-05-12 Simple Turbojet 教學模組研究目標

## 研究目標

把 pyCycle 範例 `example_cycles/simple_turbojet.py` 轉為「課堂可獨立使用」的
教學模組，讓學生在最少配置下完成：

1. 用 PySide6 GUI 改變設計點參數，觀察 cycle 收斂。
2. 讀懂 OpenMDAO 自動產生的 `n2.html` / `inputs.html`，學會用它們做架構分析。
3. 透過 T-S、P-h 圖、元件特性圖認識循環熱力學意義。
4. 把所有輸出（文字、PDF、PNG、HTML）收斂到單一資料夾，便於繳交與比對。

## 與第一階段（CFM56-7B HBTF）的差異

| 面向 | HBTF Reference UI | Simple Turbojet GUI |
|---|---|---|
| 模型複雜度 | 雙轉子高旁通比渦扇 | 單軸渦輪噴射 |
| UI 範圍 | Ribbon + 多分頁工作台 | 單視窗 + Tab |
| 報告流程 | 比對 CFM56-7B 公開資料 | 自我比較設計點與離設計點 |
| 部署單位 | `src/pycycle_edu_ui/` package | `tutorials/simple_turbojet/` 教材 |
| 目標讀者 | 高年級實作課 | 入門概念課 |

## 已完成

- 模型 + GUI 單檔整合：`tutorials/simple_turbojet/simple_turbojet.py`
- 多媒體輸出（TXT、PDF、PNG、HTML）統一進 `output/`
- 雙語使用說明：`tutorials/simple_turbojet/README.md`
- 站位標籤導引線抗重疊
- OpenMDAO reports 自動扁平化

## 後續研究方向

1. **互動式 n2 探索教案**：撰寫 step-by-step 練習，要求學生在 `n2.html` 上找出
   特定 balance 變數的回授路徑並回答熱力學問題。
2. **離設計點工況 sweep**：把 OD0 / OD1 改成 GUI 可調，做 alt × MN 二維 sweep，
   匯出推力地圖。
3. **教材化 Jupyter notebook**：將 README 內的範例情境改寫為可執行 notebook，
   降低 GUI 不可用環境的進入門檻。
4. **單元 + UI smoke test**：加入 Playwright/pytest-qt 的最小驗證，確保未來
   upstream pyCycle 更新時不會默默壞掉。

## 注意事項

- `upstream/pyCycle` 仍為唯讀。
- 本模組刻意維持 0 個 mandatory PySide6 以外的圖形相依，避免課堂工作站環境衝突。
- OpenMDAO 3.40 已移除 `set_reports_dir`，目前用 `os.chdir(OUT_DIR)` + 跑完後
  搬檔的策略；未來如 3.41+ 提供官方 API 應改用之。
