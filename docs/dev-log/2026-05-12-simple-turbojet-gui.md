# 2026-05-12 Simple Turbojet GUI

## Context

- User requested a fresh uv `.venv` using Python 3.12.
- The project is being renamed to `pyCycle_GUI` and the GitHub remote is moving to `https://github.com/LostSunset/pyCycle_GUI`.
- User requested a new PySide6 GUI for `tutorials/simple_turbojet/simple_turbojet.py`.
- GUI, generated PDF reports, generated map PDFs, and `simple_turbojet_out` outputs must show bilingual English-first / Traditional-Chinese-second text.
- `upstream/pyCycle` must remain read-only.
- User later requested a full UI reset: delete the current UI layer completely and restart UI design later.

## GitNexus analysis

- Command:
  - `npx gitnexus analyze --embeddings`
  - `npx gitnexus clean --force`
  - `npx gitnexus analyze`
- Result:
  - The first `--embeddings` run failed during finalization because the GitNexus registry entry was not added.
  - After cleaning, another `--embeddings` run timed out.
  - Fallback `npx gitnexus analyze` succeeded: 3,024 nodes, 4,333 edges, 72 clusters, 37 flows.
  - Impact analysis before editing existing symbols:
    - `main` in `src/pycycle_edu_ui/main.py`: LOW risk, 1 direct file caller.
    - `MainWindow` in `src/pycycle_edu_ui/views/main_window.py`: LOW risk, 1 direct importer.

## Changes

- Created design and implementation plan:
  - `docs/superpowers/specs/2026-05-12-simple-turbojet-gui-design.md`
  - `docs/superpowers/plans/2026-05-12-simple-turbojet-gui.md`
- Removed the UI design and plan files after the full UI reset request.
- Updated project identity and environment:
  - `pyproject.toml`
  - `.gitignore`
  - `README.md`
  - Git remote `origin` now points to `https://github.com/LostSunset/pyCycle_GUI`.
- Added simple turbojet runner/report/view files:
  - `src/pycycle_edu_ui/runner/simple_turbojet_runner.py`
  - `src/pycycle_edu_ui/runner/scripts/run_simple_turbojet_once.py`
  - `src/pycycle_edu_ui/simple_turbojet_report.py`
  - `src/pycycle_edu_ui/views/simple_turbojet_window.py`
- Updated main GUI shell:
  - `src/pycycle_edu_ui/main.py`
  - `src/pycycle_edu_ui/views/main_window.py`
- Removed retired educational/HBTF GUI support:
  - `src/pycycle_edu_ui/runner/hbtf_runner.py`
  - `src/pycycle_edu_ui/runner/scripts/run_hbtf_once.py`
  - `src/pycycle_edu_ui/reports.py`
- Removed all active UI source files and the GUI entrypoint:
  - `src/pycycle_edu_ui/main.py`
  - `src/pycycle_edu_ui/theme.py`
  - `src/pycycle_edu_ui/widgets.py`
  - `src/pycycle_edu_ui/views/__init__.py`
  - `src/pycycle_edu_ui/views/main_window.py`
  - `src/pycycle_edu_ui/views/simple_turbojet_window.py`
  - `tests/test_main_interrupt.py`
- Removed GUI dependencies and script entrypoint from `pyproject.toml`; `uv sync --python 3.12` uninstalled PySide6, QFluentWidgets, and pyqtgraph.
- Removed old auxiliary virtual environment:
  - `.venv-pycycle312`
- Retained CFM56-7B reference data only as archived source/reference material; it is no longer used by the GUI for defaults or comparisons.
- Added graceful CLI handling for Ctrl+C / `KeyboardInterrupt`:
  - `src/pycycle_edu_ui/main.py`
  - `tests/test_main_interrupt.py`
- Added tests:
  - `tests/test_simple_turbojet_report.py`
- Generated/updated simple turbojet outputs:
  - `tutorials/simple_turbojet/DESIGN.comp.pdf`
  - `tutorials/simple_turbojet/DESIGN.turb.pdf`
  - `tutorials/simple_turbojet/simple_turbojet_out/simple_turbojet_raw_output.txt`
  - `tutorials/simple_turbojet/simple_turbojet_out/simple_turbojet_bilingual_report.txt`
  - `tutorials/simple_turbojet/simple_turbojet_out/simple_turbojet_bilingual_report.pdf`
  - `tutorials/simple_turbojet/simple_turbojet_out/DESIGN.comp.pdf`
  - `tutorials/simple_turbojet/simple_turbojet_out/DESIGN.turb.pdf`

## Verification

- `uv venv --python 3.12 --clear .venv`: passed, created CPython 3.12.13 environment.
- `uv sync --python 3.12`: passed.
- `uv run pytest tests/test_simple_turbojet_report.py -v`: passed.
- `uv run python -m compileall src tests`: passed.
- `QT_QPA_PLATFORM=offscreen` MainWindow smoke test: passed; title was `pyCycle_GUI Professional Workbench / pyCycle_GUI 專業工作台`, stack count was 1 after retiring the old educational/HBTF GUI pages.
- `uv run python -c "from pycycle_edu_ui.runner.simple_turbojet_runner import run_simple_turbojet, SimpleTurbojetInputs; ..."`: passed; parsed 3 points and generated 3 PDF artifacts.
- `./scripts/verify-upstream-submodule.ps1`: passed; upstream submodule is clean and unchanged.
- `mcp__gitnexus__.detect_changes({repo: "pyCycle_edu", scope: "all"})`: reported high aggregate risk across the dirty worktree. The report includes pre-existing modified `AGENTS.md` and `CLAUDE.md` plus this task's `README.md`, `main.py`, and `main_window.py` changes; the pre-edit symbol impact checks for the touched code symbols were LOW.
- `Get-ChildItem -Force -Directory | Where-Object { $_.Name -like '.venv*' }`: confirmed only `.venv` remains after deleting `.venv-pycycle312`.
- `uv run pytest tests/test_main_interrupt.py -v`: first failed with uncaught `KeyboardInterrupt`, then passed after `main()` returned exit code 130.
- `uv run pytest tests/test_simple_turbojet_report.py tests/test_main_interrupt.py -v`: passed, 3 tests.
- Full UI reset verification:
  - `rg "PySide6|QApplication|QWidget|QMainWindow|qfluentwidgets|pyqtgraph|MetricCard|FlowDiagram|views|theme|widgets" src tests pyproject.toml`: no matches.
  - `uv run python -c "import importlib.util; ..."`: `PySide6`, `pyqtgraph`, and `qfluentwidgets` all returned `None`.
  - `rg "pyside|pyqtgraph|qfluent|shiboken" uv.lock`: no matches.
  - `uv run python -m compileall src tests`: passed after UI removal.
  - `uv run pytest tests/test_simple_turbojet_report.py -v`: passed, 2 tests.
  - Simple turbojet runner smoke: passed; parsed 3 points and generated `DESIGN.comp.pdf`, `DESIGN.turb.pdf`, and `simple_turbojet_bilingual_report.pdf`.

## Risks / follow-up

- The simple turbojet runner emits a pyCycle/OpenMDAO runtime warning from upstream thermodynamics code: `RuntimeWarning: invalid value encountered in sqrt`. The run still converged and produced parsed results.
- The bilingual map PDFs are generated by the GUI/report layer as bilingual summary plots named `DESIGN.comp.pdf` and `DESIGN.turb.pdf`; future work can add deeper native pyCycle map annotation if needed.

---

## 2026-05-12 (late) — Tutorial GUI release v0.2.0

### Context

- User requested a brand-new standalone tutorial at
  `tutorials/simple_turbojet/simple_turbojet.py` with an embedded PySide6 GUI.
- Iterative refinements requested in same session: PDF outputs, flatten
  `simple_turbojet_out/` into the tutorial folder, fix overlapping station
  labels on T-S/P-h diagrams, expose OpenMDAO `n2.html` / `inputs.html`,
  publish a complete bilingual user guide, and run the finalization
  checklist with version bump and release.

### GitNexus analysis

- Command: relied on GitNexus context surfaced by the editing environment
  (PreToolUse hook reported the related symbols across `tutorials/` and
  upstream `example_cycles/simple_turbojet.py`).
- Result: edit scope confined to `tutorials/simple_turbojet/` only. The
  runner (`src/pycycle_edu_ui/runner/scripts/run_simple_turbojet_once.py`)
  still imports `MPTurbojet`, `viewer`, `comprehensive_performance_summary`
  from the tutorial module, so those public symbols were preserved.

### Changes

- New: `tutorials/simple_turbojet/simple_turbojet.py` — pyCycle model
  classes retained verbatim, plus `solve_problem`, `draw_ts_diagram`,
  `draw_ph_diagram`, `draw_comparison`, `save_component_maps`,
  `save_summary_pdf`, `_flatten_openmdao_reports`, and a `launch_gui`
  PySide6 entry point.
- New: `tutorials/simple_turbojet/README.md` — bilingual user guide with
  `inputs.html` / `n2.html` walkthroughs and engineering scenarios.
- New: `CHANGELOG.md` (project-wide).
- New: `docs/sessions/2026-05-12-simple-turbojet-gui-release-session.md`.
- New: `docs/research/2026-05-12-simple-turbojet-tutorial.md`.
- Updated: `pyproject.toml`, `src/pycycle_edu_ui/__init__.py` — version
  `0.1.0` → `0.2.0`.
- Updated: `.gitignore` — add `output/`, `.gitnexus/`, `.pytest_cache/`,
  `.agents/`, and `.env*` / `*.pem` / `*.key` / `secrets.*` patterns.
- Updated: `README.md`, `CLAUDE.md`, `AGENTS.md`, `MEMORY.md` — reflect
  the new tutorial entry point and v0.2.0 state.

### Verification

- `python -c "import ast; ast.parse(open(...).read())"` — module parses.
- `python -c "import simple_turbojet"` — imports cleanly with PySide6
  installed via `uv pip install PySide6`.
- Headless solve: `solve_problem(...)` → `Fn_DESIGN ≈ 11799.998 lbf`
  (target 11800 lbf).
- `output/` confirmed as the **only** generated subfolder; OpenMDAO's
  nested `<prob>_out/` no longer remains after `_flatten_openmdao_reports`.
- Regenerated T-S and P-h PNGs visually verified — station labels no
  longer overlap.
- Secret scan: no API keys, tokens, or passwords found in tracked text
  files.
- `./scripts/verify-upstream-submodule.ps1` — clean.

### Risks / follow-up

- `os.chdir(OUT_DIR)` inside `solve_problem` mutates process CWD. Acceptable
  because the GUI is single-shot and the headless runner already sets its
  own CWD via `subprocess`. Future entry points should remember this.
- Manual `_flatten_openmdao_reports` should be replaced if OpenMDAO 3.41+
  ever adds an official redirect API.
