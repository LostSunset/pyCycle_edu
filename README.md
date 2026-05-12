# pyCycle_GUI

`pyCycle_GUI` is a professional workspace around upstream pyCycle.
The current UI layer has been intentionally removed so the GUI can be redesigned from a clean slate.

`upstream/pyCycle` is a read-only reference submodule. Do not edit files inside it or update its gitlink unless explicitly requested.

## Current State

- GUI: reset and not currently implemented.
- Kept: simple turbojet runner and bilingual report/PDF generation foundation.
- Kept: CFM56-7B reference material as archived data only.
- Removed from the active app: educational GUI, HBTF GUI, CFM56-7B comparison/default workflow, PySide6 entrypoint.

## Environment

Use Python 3.12 through `uv`.

```powershell
uv venv --python 3.12 --clear .venv
uv sync --python 3.12
```

Only `.venv` should be used for this project.

## Repository Structure

| Path | Purpose |
|---|---|
| `upstream/pyCycle/` | Read-only upstream pyCycle submodule. |
| `src/pycycle_edu_ui/runner/` | Local runner code for pyCycle cases. |
| `src/pycycle_edu_ui/simple_turbojet_report.py` | Bilingual simple turbojet report/PDF generation. |
| `tutorials/simple_turbojet/` | Local simple turbojet case and generated bilingual outputs. |
| `Reference_sources/` | Archived external reference sources, including retained CFM56-7B materials. |
| `docs/dev-log/` | Required development log entries. |
| `scripts/` | Repository maintenance and verification scripts. |

## Simple Turbojet Outputs

The retained simple turbojet pipeline writes outputs under:

```text
tutorials/simple_turbojet/simple_turbojet_out/
```

Important generated files:

| File | Purpose |
|---|---|
| `simple_turbojet_bilingual_report.txt` | Bilingual text report. |
| `simple_turbojet_bilingual_report.pdf` | Bilingual PDF report. |
| `DESIGN.comp.pdf` | Bilingual compressor summary PDF. |
| `DESIGN.turb.pdf` | Bilingual turbine summary PDF. |
| `simple_turbojet_raw_output.txt` | Raw pyCycle/OpenMDAO output capture. |

## Required Workflow

Before analysis or code edits, run:

```powershell
npx gitnexus analyze --embeddings
```

Before committing, run:

```powershell
./scripts/verify-upstream-submodule.ps1
```

Every meaningful development task must be recorded in `docs/dev-log/`.
