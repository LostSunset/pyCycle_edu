# 2026-05-11 Ribbon Engineering UI

## Context

- User requested that the PySide6 app feel like a professional engineering analysis desktop application.
- UI text must not use the phrase `實戰`.
- Main interactions should move to a Microsoft Office-like Ribbon, with engineering input fields and background pyCycle execution.

## GitNexus analysis

- Command: `npx gitnexus analyze --embeddings`
- Result: timed out after about 604 seconds in this session.
- Impact analysis attempted for `MainWindow` and `run_high_bypass_turbofan`; GitNexus reported `.gitnexus` was locked by the timed-out analysis process.
- Alternative checks used: local `rg` search, py_compile, pyCycle runner execution, Qt offscreen smoke test, Qt offscreen screenshot review, report generation, `gitnexus detect_changes`, and upstream submodule verification.

## Changes

- Reworked the main PySide6 window into a Ribbon-style engineering analysis UI.
- Renamed the application window to `pyCycle CFM56-7B 工程分析工作台`.
- Removed user-facing `實戰` wording from the app and reference answer page.
- Added editable inputs for Mach, altitude, T4/Tt4, Fn target, BPR, Fan PR, LPC PR, HPC PR, and percent thrust.
- Added input validation with ranges and a pressure-ratio sanity check.
- Added `EngineInputs` and passed UI input values to the pyCycle wrapper through environment variables.
- Changed pyCycle execution to a background `QThread`, so the UI remains responsive while solving.
- Added status bar messages, elapsed time display, and output path reporting.
- Added Ribbon UI screenshots for pre-run and post-run inspection.

## Verification

- `uv run python -m py_compile ...`: passed.
- `uv run python -c "from pycycle_edu_ui.runner.hbtf_runner import EngineInputs, run_high_bypass_turbofan; ..."`: passed; parsed 2 points in about 49.8 seconds.
- Qt offscreen smoke test: passed; window title was `pyCycle CFM56-7B 工程分析工作台`, stack count was 4, and input count was 9.
- Qt offscreen screenshot export: passed; generated `ribbon_ui_offscreen.png`.
- Qt offscreen background-run test: passed; pyCycle solved in the background, parsed 2 points, updated status, and generated `ribbon_ui_after_run.png`.
- Traditional Chinese report generation: passed.
- `uv sync --python 3.12`: passed.
- `gitnexus detect_changes(scope="all")`: high risk; affected processes were the expected core UI/runner/report flows for this Ribbon and background-execution change.
- `gitnexus detect_changes(scope="staged")`: high risk; affected processes remained the expected core UI/runner/report flows.
- `./scripts/verify-upstream-submodule.ps1`: passed; upstream submodule is clean and unchanged.

## Risks / follow-up

- The current pyCycle solve still takes about 49 seconds on this machine; background execution keeps the UI usable, but future work should add cancellation and progress detail.
- The CFM56-7B comparison remains an engineering reference comparison, not an OEM-calibrated engine deck.
