# MEMORY

## Project Identity

- Repository: `D:\45_pyCycle_edu`
- GitHub wrapper repository: `LostSunset/pyCycle_edu`
- Upstream reference submodule: `upstream/pyCycle`
- Upstream submodule must remain read-only unless the owner explicitly requests an upstream sync.

## Standing Rules

- Run `npx gitnexus analyze --embeddings` before meaningful analysis or edits.
- Run `./scripts/verify-upstream-submodule.ps1` before committing.
- Record meaningful development tasks in `docs/dev-log/`.
- Store or record external sources in `Reference_sources/` before using them for validation.
- Every time a PPTX is generated or modified, export it to PNG preview images and visually inspect the slides before claiming the deck is ready. Check for text outside frames, clipped text, distorted images, overly small text, and poor text/image balance.

## Fixed Finalization Checklist

For every version or milestone, remember these 9 steps:

0. Commit and push.
1. Decide whether the version should be updated.
2. Decide whether a new Release should be published.
3. Decide whether Markdown files under `docs/` should be updated or added.
4. Decide whether `README.md` should be updated.
5. Decide whether `CLAUDE.md` and `AGENTS.md` should be updated.
6. Decide again whether additional Markdown files under `docs/` are needed.
7. Follow the rules to update developer logs and add a session note.
8. Decide whether research goals and research logs should be updated.

## Current Teaching Direction

- Teach students how to prompt AI to manage `uv` / `.venv`, use pyCycle, and plan a PySide6 UI approximating entry-level GasTurb workflows.
- First case study: CFM56-7B-class high-bypass turbofan.
- Use upstream pyCycle examples as reference, especially `upstream/pyCycle/example_cycles/high_bypass_turbofan.py`.
- Do not claim the pyCycle example is a calibrated CFM56-7B engine deck.

## Current Assets

- Teaching deck: `docs/slides/pycycle_ai_prompting_course.pptx`
- Deck generator: `docs/slides/build_pycycle_ai_prompting_ppt.py`
- Deck visual assets: `docs/slides/assets/`
- Source manifest: `Reference_sources/source_manifest.md`
- Main dev log: `docs/dev-log/2026-05-11-pycycle-ai-prompting-ppt.md`

## Version / Release State

- No project version file exists yet.
- No GitHub Release should be created for the current teaching-deck work unless a version/tag policy is introduced.
