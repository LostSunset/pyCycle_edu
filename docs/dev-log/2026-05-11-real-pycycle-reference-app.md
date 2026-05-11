# 2026-05-11 Real pyCycle Reference App

## Context

- User clarified that the `Reference_answers/` app must be a real usable reference app, not a teaching placeholder.
- The app must execute pyCycle, compare pyCycle outputs against CFM56-7B reference data, show comparison charts, and generate a Traditional Chinese report because pyCycle's viewer output is English.

## GitNexus analysis

- Command: `npx gitnexus analyze --embeddings`
- Result: timed out after about 604 seconds in this session.
- Fallback command: `npx gitnexus analyze`
- Result: timed out after about 304 seconds in this session.
- Impact analysis attempts for `EngineCase`, `estimate_reference_result`, and `MainWindow` failed because `.gitnexus` was locked by the timed-out analysis process. Final verification therefore uses local search, targeted pyCycle execution, compile checks, UI smoke checks, staged review, and `gitnexus detect_changes` if the lock is released before commit.

## Changes

- Reworked the PySide6 app from a teaching estimator into a real pyCycle reference app.
- Added a pyCycle runner that imports upstream `MPhbtf` and `viewer` from `high_bypass_turbofan.py`, runs DESIGN and one OD point, and saves pyCycle's English `hbtf_view.out`.
- Added parsing for pyCycle performance rows: Mach, altitude, W, Fn, Fg, ram drag, OPR, TSFC, and BPR.
- Added CFM56-7B reference metrics for thrust range, BPR, OPR, and fan diameter.
- Added Traditional Chinese Markdown report generation with source notes and model limitations.
- Updated the UI to show real pyCycle values, CFM56-7B comparison table, pyqtgraph comparison plot, pyCycle point table, and report controls.
- Constrained the project to Python 3.10-3.12, NumPy 1.x, and OpenMDAO 3.40 to avoid pyCycle/OpenMDAO failures seen on Python 3.14 and NumPy 2.x.
- Removed the old teaching-estimate model module.

## Verification

- `UV_PROJECT_ENVIRONMENT=.venv-pycycle312 uv sync --python 3.12`: passed.
- `UV_PROJECT_ENVIRONMENT=.venv-pycycle312 uv run python -m py_compile ...`: passed.
- `UV_PROJECT_ENVIRONMENT=.venv-pycycle312 uv run python -c "from pycycle_edu_ui.runner.hbtf_runner import run_high_bypass_turbofan; ..."`: passed; parsed 2 pyCycle points.
- Parsed DESIGN point: Fn `5900.0 lbf`, OPR `30.094`, TSFC `0.63072`, BPR `5.105`.
- Qt offscreen `QApplication` / `MainWindow` smoke test: passed.
- Qt offscreen run plus screenshot export: passed; generated `Reference_answers/pycycle_ui_ux_reference/screenshots/main_window_after_pycycle.png`.
- `save_chinese_report(...)`: passed; generated a Traditional Chinese Markdown report.
- `gitnexus detect_changes(scope="all")`: medium risk; affected processes were existing UI initialization/report flows, expected for replacing the placeholder UI flow with the real pyCycle runner.
- `gitnexus detect_changes(scope="staged")`: medium risk; affected processes remained the expected UI initialization/report flows.
- `./scripts/verify-upstream-submodule.ps1`: passed; upstream submodule is clean and unchanged.

## Risks / follow-up

- The app uses pyCycle's high-bypass turbofan example as an engineering comparison scaffold, not a calibrated CFM56-7B engine deck.
- CFM56-7B sea-level static thrust is not directly comparable to pyCycle's cruise DESIGN point; the UI and report label this explicitly.
- Next step: add a progress-threaded runner so the UI remains responsive during the 45-60 second pyCycle solve.
