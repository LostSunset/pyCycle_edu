# pyCycle_GUI

`pyCycle_GUI` is a professional workspace around upstream pyCycle.
**v0.2.0** ships the first end-user tutorial: a self-contained PySide6 GUI
for a simple single-spool turbojet, with bilingual user documentation.

`upstream/pyCycle` is a read-only reference submodule. Do not edit files inside
it or update its gitlink unless explicitly requested.

## Current State

- **Tutorial GUI (new in v0.2.0):** `tutorials/simple_turbojet/simple_turbojet.py`
  — PySide6 GUI that runs the pyCycle `MPTurbojet` model in a worker thread,
  shows embedded T-S / P-h / Comparison charts, and writes every artefact
  (TXT, PDF, PNG, HTML) into a single `output/` folder.
- **Bilingual user guide:** `tutorials/simple_turbojet/README.md` — covers how
  to read `inputs.html` and `n2.html` with engineering scenarios.
- **Workbench package:** `src/pycycle_edu_ui/` — runner + bilingual
  report/PDF generation. The interactive Ribbon/HBTF UI shell has been
  retired pending redesign.
- **Reference assets:** archived CFM56-7B reference material remains in
  `Reference_sources/`.

## Environment

Use Python 3.12 through `uv`.

```powershell
uv venv --python 3.12 --clear .venv
uv sync --python 3.12
uv pip install PySide6  # required for the tutorial GUI
```

Only `.venv` should be used for this project.

## Launch the Simple Turbojet GUI

```powershell
$env:PYTHONPATH = "D:\45_pyCycle_GUI\upstream\pyCycle;D:\45_pyCycle_GUI\tutorials\simple_turbojet"
python D:\45_pyCycle_GUI\tutorials\simple_turbojet\simple_turbojet.py
```

After pressing **▶ Run**, all files appear under
`tutorials/simple_turbojet/output/`. See the [tutorial README](tutorials/simple_turbojet/README.md)
for a full walkthrough of every output file, including a complete guide to
`inputs.html` and the OpenMDAO `n2.html` N² diagram.

## Repository Structure

| Path | Purpose |
|---|---|
| `upstream/pyCycle/` | Read-only upstream pyCycle submodule. |
| `tutorials/simple_turbojet/` | **Standalone tutorial GUI + bilingual user guide.** |
| `tutorials/simple_turbojet/output/` | Generated artefacts (gitignored). |
| `src/pycycle_edu_ui/runner/` | Headless runners that drive pyCycle cases. |
| `src/pycycle_edu_ui/simple_turbojet_report.py` | Bilingual report/PDF generator. |
| `Reference_sources/` | Archived external reference sources. |
| `docs/dev-log/` | Required development log entries. |
| `docs/sessions/` | Per-session hand-off notes. |
| `docs/research/` | Research goals and progress logs. |
| `docs/slides/` | Teaching deck generator and PPTX outputs. |
| `scripts/` | Repository maintenance and verification scripts. |
| `CHANGELOG.md` | Version history (semver). |

## Outputs Produced by the Tutorial GUI

Every run regenerates these inside `tutorials/simple_turbojet/output/`:

| File | Purpose |
|---|---|
| `simple_turbojet_summary.txt` / `.pdf` | Inputs, solver log, performance summary. |
| `simple_turbojet_ts_diagram.png` / `.pdf` | Temperature-entropy cycle. |
| `simple_turbojet_ph_diagram.png` / `.pdf` | Pressure-enthalpy cycle. |
| `simple_turbojet_comparison.png` / `.pdf` | DESIGN vs OD0 vs OD1 four-panel. |
| `simple_turbojet_compressor_map_DESIGN_*.png` / `.pdf` | Compressor map with op point. |
| `simple_turbojet_turbine_map_DESIGN_*.png` / `.pdf` | Turbine map with op point. |
| `DESIGN.comp.pdf` / `DESIGN.turb.pdf` | pyCycle component summary PDFs. |
| `inputs.html` | OpenMDAO input variable inventory. |
| `n2.html` | OpenMDAO interactive N² system structure diagram. |

## Required Workflow

Before committing, run:

```powershell
./scripts/verify-upstream-submodule.ps1
```

Every meaningful development task must be recorded in `docs/dev-log/`.

## Versioning

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
See `CHANGELOG.md` for the full history. Current version: **0.2.0**.
