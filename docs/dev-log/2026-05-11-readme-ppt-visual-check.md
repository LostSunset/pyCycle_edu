# 2026-05-11 README and PPT Visual Check Rule

## Context

- User requested that `README.md` be converted to Traditional Chinese.
- User reported that generated PPTX decks must always be exported to images for visual checking because prior slides had text outside frames and stretched images.
- User asked to remember the fixed 9-step finalization checklist for future version/milestone work.

## GitNexus analysis

- Command:
  - `npx gitnexus analyze --embeddings`
- Result:
  - Repository indexed successfully.
  - Result summary: 2,594 nodes, 3,676 edges, 53 clusters, 22 flows.
  - Semantic embeddings use exact-scan fallback because VECTOR index is not enabled on this platform.
- Impact analysis:
  - `add_picture` in `docs/slides/build_pycycle_ai_prompting_ppt.py`
  - Risk: LOW
  - Direct affected symbol: `make_deck`
  - Affected process/module: slide generation only.

## Changes

- Rewrote `README.md` in Traditional Chinese.
- Updated `MEMORY.md` with:
  - PPTX-to-PNG visual inspection rule.
  - The fixed 9-step finalization checklist.
- Updated `AGENTS.md` and `CLAUDE.md` with the PPTX visual preview requirement and refreshed GitNexus index counts.
- Updated `docs/slides/build_pycycle_ai_prompting_ppt.py` so inserted pictures preserve aspect ratio inside the requested bounding box.
- Added `docs/slides/export-pptx-preview.ps1` to export PPTX decks into PNG previews.
- Regenerated `docs/slides/pycycle_ai_prompting_course.pptx`.
- Exported preview images under `docs/slides/preview_png/` for visual inspection evidence.
- Added `docs/sessions/2026-05-11-readme-ppt-visual-check-session.md`.
- Updated `docs/research/2026-05-11-ai-prompting-pycycle-ui.md` with the visual inspection requirement.

## Verification

- `uv run --with python-pptx --with pillow python docs/slides/build_pycycle_ai_prompting_ppt.py`
  - Result: regenerated `docs/slides/pycycle_ai_prompting_course.pptx`.
- `./docs/slides/export-pptx-preview.ps1`
  - Result: exported 21 preview images from 21 slides to `docs/slides/preview_png`.
- PowerPoint COM open check:
  - Result: `PowerPoint open check slides=21`.
- `./scripts/verify-upstream-submodule.ps1`
  - Result: `Upstream submodule is clean and unchanged.`
- GitNexus `detect_changes` with `scope: all`
  - Result: risk level `medium`.
  - Changed scope includes README, MEMORY, AGENTS/CLAUDE workflow instructions, research notes, and slide generator symbols.
  - Affected process reported: `Two_col -> Set_font`, related to slide generation only.
- Manual preview review:
  - Reviewed the contact sheet and key slides including slides 1, 10, and 12.
  - Confirmed generated images now preserve aspect ratio after the `add_picture` fix.
  - Confirmed visual previews are available for follow-up review.

## Risks / follow-up

- Some prompt-heavy slides remain dense. The deck is now visually inspectable through exported PNGs, but a future teaching polish pass should split long prompt cards into multiple slides or move full prompts into speaker notes/handouts.
- No version bump and no GitHub Release are required because this is documentation and teaching-material maintenance.
