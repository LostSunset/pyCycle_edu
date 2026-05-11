# 2026-05-11 PySide6 UI UX

## Context

- User requested a reference-answer folder and the first PySide6 UI/UX implementation for pyCycle Edu.
- The UI should use a suitable online template/library, apply a Claude beige visual style, and support the future pyCycle workflow.

## GitNexus analysis

- Command: `npx gitnexus analyze --embeddings`
- Result: completed successfully with exact-scan embedding fallback; GitNexus updated the repository index to 2616 symbols, 3698 relationships, and 22 execution flows.

## Changes

- Added `pyproject.toml` with `uv`-managed dependencies for PySide6, PySide6-Fluent-Widgets, pyqtgraph, and numpy.
- Added `src/pycycle_edu_ui/` with a first PySide6 workbench UI.
- Added `Reference_answers/` with UI/UX reference answers and staged prompts.
- Added a PySide6 UI/UX research note and session handoff.
- Updated README with the new reference-answer and UI launch workflow.

## Verification

- `uv run python -m py_compile src\pycycle_edu_ui\main.py src\pycycle_edu_ui\theme.py src\pycycle_edu_ui\models.py src\pycycle_edu_ui\widgets.py src\pycycle_edu_ui\views\main_window.py`: passed.
- `QT_QPA_PLATFORM=offscreen` QApplication/MainWindow smoke test: passed; window title was `pyCycle Edu Workbench` and the stack contained 3 pages.
- `QT_QPA_PLATFORM=offscreen` UI screenshot export: passed; generated `Reference_answers/pycycle_ui_ux_reference/screenshots/main_window_offscreen.png`.
- `gitnexus detect_changes(scope="all")`: low risk; affected process count was 0.
- `gitnexus detect_changes(scope="staged")`: low risk; affected process count was 0 after staging.
- `./scripts/verify-upstream-submodule.ps1`: passed; upstream submodule is clean and unchanged.

## Risks / follow-up

- First UI result values are teaching estimates only; the next milestone must connect to a pyCycle wrapper.
- QFluentWidgets is used opportunistically with Qt Widgets fallback; visual polish should be checked on the target classroom machines.
