# 2026-05-11 README and PPT Visual Check Session

## Summary

- Converted the repository README to Traditional Chinese.
- Added a standing rule that every generated or modified PPTX must be exported to PNG preview images and visually inspected.
- Added a PowerPoint preview export script.
- Updated the PPT generator to preserve image aspect ratio.
- Remembered the user's fixed 9-step finalization checklist in `MEMORY.md`.

## Files Changed

- `README.md`
- `MEMORY.md`
- `AGENTS.md`
- `CLAUDE.md`
- `docs/slides/build_pycycle_ai_prompting_ppt.py`
- `docs/slides/export-pptx-preview.ps1`
- `docs/slides/pycycle_ai_prompting_course.pptx`
- `docs/slides/preview_png/`
- `docs/dev-log/2026-05-11-readme-ppt-visual-check.md`
- `docs/research/2026-05-11-ai-prompting-pycycle-ui.md`

## Validation

- GitNexus analysis was rerun and reported an updated index.
- GitNexus impact analysis for `add_picture` reported LOW risk.
- PPTX was regenerated.
- Preview PNGs were exported through PowerPoint COM.
- Contact sheet and representative slides were visually checked.

## Follow-up

- Future PPT iterations should reduce dense prompt cards by splitting content across slides or moving full prompt text into handouts.

