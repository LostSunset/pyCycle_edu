# Stage 02 Prompt: uv and PySide6 Setup

## 給 AI 的提示詞

```text
請在這個 repository 中建立 PySide6 UI 專案骨架，並使用 uv 管理環境。
限制：
1. 不可以修改 upstream/pyCycle。
2. 新增 pyproject.toml，dependencies 至少包含 PySide6、PySide6-Fluent-Widgets、pyqtgraph、OpenMDAO。
3. UI 程式放在 src/pycycle_edu_ui/。
4. 建立一個可執行入口 pycycle-edu-ui。
5. UI 要有 Claude 米色風格，字體要大，適合教室投影與年長學生閱讀。
6. 建立 Reference_answers/pycycle_ui_ux_reference/，保存提示詞與參考答案。
7. Python 請使用 3.12，NumPy 鎖定 1.x，避免 pyCycle/OpenMDAO 在過新的 Python/NumPy 上失敗。
8. 完成後執行能在 offscreen 模式下建立 QApplication 與 MainWindow 的驗證。
```

## 預期結果

- `uv sync --python 3.12` 可以建立可重現環境。
- `uv run pycycle-edu-ui` 可以開啟 UI。
- `uv run python -m pycycle_edu_ui.main` 可以從模組啟動。
- 程式碼不依賴修改 upstream pyCycle。
