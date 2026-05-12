# MEMORY

## Project Identity

- Repository: `D:\45_pyCycle_GUI`
- GitHub wrapper repository: `LostSunset/pyCycle_GUI`
- Upstream reference submodule: `upstream/pyCycle`
- Upstream submodule must remain read-only unless the owner explicitly requests an upstream sync.

## Standing Rules

- Run `./scripts/verify-upstream-submodule.ps1` before committing.
- Record meaningful development tasks in `docs/dev-log/`.
- Store or record external sources in `Reference_sources/` before using them for validation.
- Every time a PPTX is generated or modified, export it to PNG preview images and visually inspect the slides before claiming the deck is ready. Check for text outside frames, clipped text, distorted images, overly small text, and poor text/image balance.
- Never push API keys, credentials, `.env`, `.pem`, `.key`, or any private user data. `.gitignore` codifies the patterns; scan the staged tree before any push.

## Fixed Finalization Checklist

For every version or milestone, remember these 9 steps:

0. Commit and push.
1. Decide whether the version should be updated.
2. Decide whether a new Release should be published.
3. Decide whether Markdown files under `docs/` should be updated or added.
4. Decide whether `README.md` should be updated.
5. Decide whether `CLAUDE.md`, `MEMORY.md`, and `AGENTS.md` should be updated.
6. Decide again whether additional Markdown files under `docs/` are needed.
7. Follow the rules to update developer logs and add a session note.
8. Decide whether research goals and research logs should be updated.
9. Commit and push the release work; tag if a version was bumped.

## Current Teaching Direction

- Primary tutorial (v0.2.0): `tutorials/simple_turbojet/simple_turbojet.py`
  — standalone PySide6 GUI driving the pyCycle `MPTurbojet` model.
- Bilingual user guide: `tutorials/simple_turbojet/README.md`.
- Secondary case study (CFM56-7B-class HBTF) remains in `homewoks/` and the
  archived reference materials; the interactive HBTF GUI is on hold.
- Do not claim any pyCycle example is a calibrated production engine deck.

## Current Assets

- Tutorial GUI: `tutorials/simple_turbojet/simple_turbojet.py`
- Tutorial user guide: `tutorials/simple_turbojet/README.md`
- Headless runner: `src/pycycle_edu_ui/runner/simple_turbojet_runner.py`
- Report generator: `src/pycycle_edu_ui/simple_turbojet_report.py`
- Teaching deck: `docs/slides/pycycle_ai_prompting_course.pptx`
- Deck generator: `docs/slides/build_pycycle_ai_prompting_ppt.py`
- Source manifest: `Reference_sources/source_manifest.md`
- Changelog: `CHANGELOG.md`

## Version / Release State

- Current version: **0.2.0** (`pyproject.toml`, `src/pycycle_edu_ui/__init__.py`).
- Versioning policy: Semantic Versioning. Notable changes recorded in `CHANGELOG.md`.
- Release v0.2.0 — Simple Turbojet PySide6 GUI tutorial, bilingual user
  guide, flattened `output/`, OpenMDAO reports included.
- Future release decisions live with this checklist; bump version + tag
  whenever a milestone ships.
