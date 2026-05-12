# Changelog

All notable changes to `pyCycle_GUI` will be documented in this file.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] — 2026-05-12

### Added

- **Simple turbojet PySide6 GUI tutorial** at `tutorials/simple_turbojet/simple_turbojet.py`.
  Self-contained module bundling the pyCycle `Turbojet` / `MPTurbojet` model with
  an embedded PySide6 interface. The solver runs in a Qt worker thread so the UI
  stays responsive.
- Embedded matplotlib plots for **T-S diagram**, **P-h diagram**, and a
  **four-panel comparison** of DESIGN / OD0 / OD1 working points.
- Station labels on the T-S and P-h diagrams use directional offsets with
  leader lines so neighbouring stations (0/1, 2/3, 4/5) no longer overlap.
- One-stop output folder `tutorials/simple_turbojet/output/` for every
  artefact: bilingual TXT/PDF summary, three chart pairs (PNG + PDF),
  compressor/turbine map pairs, OpenMDAO `n2.html` and `inputs.html`.
- Comprehensive bilingual user guide at `tutorials/simple_turbojet/README.md`
  covering how to read `inputs.html` and `n2.html` with concrete engineering
  scenarios (takeoff thrust verification, cruise TSFC review, compressor
  trade study, classroom usage).
- Pre-flight unit / integration tests under `tests/`.

### Changed

- OpenMDAO 3.40 auto-generated `<prob>_out/reports/` directory is flattened
  into `output/` after every run; the empty work folder is cleaned up
  automatically.
- pyCycle component-map side-effect PDFs are redirected into `output/` via
  `os.chdir` before solving.
- Repository identity is now `pyCycle_GUI` (was `pyCycle Edu`).

### Removed

- Retired ribbon / HBTF / educational PySide6 GUI scaffolding under
  `src/pycycle_edu_ui/views/` and supporting `main.py`, `theme.py`,
  `widgets.py`, `reports.py`, `runner/hbtf_runner.py`.
- Archived `Reference_answers/pycycle_ui_ux_reference/` reference deck.

### Security

- `.gitignore` updated to exclude `.env*`, `*.pem`, `*.key`, `secrets.*`,
  generated `output/`, local agent caches, and CI/lint scratch dirs.

## [0.1.0] — 2026-05-11

Initial governance, upstream pyCycle submodule wiring, AI-prompting course
slides, reference materials, and first reset of the active UI layer.
