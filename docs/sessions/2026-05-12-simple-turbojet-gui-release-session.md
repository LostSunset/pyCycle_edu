# 2026-05-12 Simple Turbojet GUI Release Session (v0.2.0)

## Summary

- Built a self-contained PySide6 GUI inside `tutorials/simple_turbojet/simple_turbojet.py`
  that runs the pyCycle `MPTurbojet` model in a Qt worker thread, embeds T-S / P-h
  / Comparison charts, and writes every artefact into a single `output/` folder.
- Fixed station-label overlap on T-S and P-h diagrams via per-station directional
  offsets and leader lines.
- Funnelled OpenMDAO 3.40's auto-generated `<prob>_out/reports/` tree into
  `output/` after each run; pyCycle map-plot side effects also land there.
- Wrote a bilingual user guide `tutorials/simple_turbojet/README.md` with concrete
  engineering use cases for `inputs.html` and `n2.html`.
- Bumped project version `0.1.0` → `0.2.0`, started `CHANGELOG.md`, and refreshed
  governance docs (README, CLAUDE.md, AGENTS.md, MEMORY.md).

## Files Changed

- `tutorials/simple_turbojet/simple_turbojet.py` *(new)*
- `tutorials/simple_turbojet/README.md` *(new — bilingual user guide)*
- `pyproject.toml`, `src/pycycle_edu_ui/__init__.py` — version bump
- `CHANGELOG.md` *(new)*
- `README.md`, `CLAUDE.md`, `AGENTS.md`, `MEMORY.md`
- `.gitignore` — add `output/`, `.gitnexus/`, `.pytest_cache/`, `.agents/`, secret patterns
- `docs/dev-log/2026-05-12-simple-turbojet-gui.md` — appended release notes
- `docs/research/2026-05-12-simple-turbojet-tutorial.md` *(new)*

## Validation

- `python -c "import simple_turbojet"` — module imports cleanly.
- Headless solve via `solve_problem(...)` — Newton converges; `Fn_DESIGN ≈ 11799.998 lbf`
  matches the 11800 lbf target.
- Confirmed `output/` is the **only** generated directory; no stray `*_out/`
  subfolder remains after `_flatten_openmdao_reports` runs.
- `inputs.html` and `n2.html` open correctly in Chrome / Edge.
- Visual check of regenerated `simple_turbojet_ts_diagram.png` and
  `simple_turbojet_ph_diagram.png` confirms station labels no longer overlap.
- `./scripts/verify-upstream-submodule.ps1` — clean.
- Secret scan across `.py` / `.md` / `.toml` / `.json` / `.yaml` files — no
  embedded API keys, tokens, or credentials found.

## Follow-up

- Consider exposing OD0 / OD1 inputs in the GUI (currently hard-coded in
  `MPTurbojet.setup`).
- Investigate replacing the manual `_flatten_openmdao_reports` heuristic with
  a future official OpenMDAO redirect API if added in 3.41+.
- Add a small Playwright / smoke test that boots the GUI head-less and
  verifies the `output/` artefact list after a Run.
