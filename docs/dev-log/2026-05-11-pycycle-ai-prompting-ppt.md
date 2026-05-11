# 2026-05-11 pyCycle AI Prompting PPT

## Context

- The project needs a Traditional Chinese teaching slide deck for students learning how to prompt AI to manage a uv `.venv`, use pyCycle, and plan a PySide6 UI approximating entry-level GasTurb workflows.
- The first teaching engine target is a mainstream high-bypass turbofan with public data, using CFM56-7B as the teaching reference and pyCycle's `high_bypass_turbofan.py` as read-only model context.
- External sources must be stored or recorded in `Reference_sources/` before use.

## GitNexus analysis

- Command:
  - `npx gitnexus analyze --embeddings`
- Result:
  - Repository indexed successfully in about 700.9 seconds.
  - Result summary: 2,433 nodes, 3,429 edges, 51 clusters, 15 flows.
  - Warnings observed: LadybugDB lock warnings during schema creation, FTS extension unavailable message, and VECTOR index fallback to exact-scan. Final index status was successful with embeddings available.
  - GitNexus context checked for `HBTF` in `upstream/pyCycle/example_cycles/high_bypass_turbofan.py`; it is treated as read-only reference content.

## Changes

- Added `Reference_sources/README.md` with source governance rules.
- Added `Reference_sources/source_manifest.md` documenting source URLs, download status, and validation use.
- Downloaded accessible sources:
  - `Reference_sources/nasa-20170000232-pycycle-openmdao.pdf`
  - `Reference_sources/openmdao-pycycle-readme.md`
  - `Reference_sources/aircraft-commerce-cfm56-7b-specs.pdf`
- Added `docs/superpowers/plans/2026-05-11-pycycle-ai-prompting-ppt-plan.md`.
- Added `docs/slides/build_pycycle_ai_prompting_ppt.py`.
- Generated `docs/slides/pycycle_ai_prompting_course.pptx`.
- Added `README.md` as the repository entry point for the education wrapper.
- Added `MEMORY.md` for cross-agent project memory.
- Added `docs/sessions/2026-05-11-ai-prompting-ppt-session.md` for handoff context.
- Added `docs/research/2026-05-11-ai-prompting-pycycle-ui.md` for research goals and progress.
- Updated `AGENTS.md` and `CLAUDE.md` GitNexus index counts from 2,423 nodes / 3,419 edges to 2,433 nodes / 3,429 edges.
- Did not modify files inside `upstream/pyCycle`.
- Version / release decision: no package version file or tag policy exists yet, so no version bump and no GitHub Release are required for this documentation/teaching-deck update.

## Verification

- `uv run --with python-pptx --with pillow python docs/slides/build_pycycle_ai_prompting_ppt.py`
  - Result: generated `D:\45_pyCycle_edu\docs\slides\pycycle_ai_prompting_course.pptx`.
- `uv run --with python-pptx python -c "from pptx import Presentation; p='D:/45_pyCycle_edu/docs/slides/pycycle_ai_prompting_course.pptx'; prs=Presentation(p); print(len(prs.slides)); print(prs.slide_width, prs.slide_height)"`
  - Result: `21` slides, widescreen 16:9 dimensions.
- `Get-ChildItem -Path 'D:\45_pyCycle_edu\Reference_sources','D:\45_pyCycle_edu\docs\slides' | Select-Object FullName,Length`
  - Result: confirmed generated PPTX, generator script, source manifest, and downloaded sources exist.
- `Get-FileHash -Algorithm SHA256 'D:\45_pyCycle_edu\docs\slides\pycycle_ai_prompting_course.pptx'`
  - Initial generated result: SHA256 `4D5A7AA1668C60956E15239879551C72363507F4A691B62769C1518A75CD32CB`.
- User reported Microsoft PowerPoint repair warning when opening the initial generated PPTX.
  - Investigation: the PPTX ZIP and XML were well-formed, and a minimal python-pptx deck opened in PowerPoint. A slide-count binary check found that adding slide 9 caused PowerPoint to reject the deck.
  - Fix: simplified slide 9 from a multi-shape pill/textbox layout to a conservative table layout, removed custom text auto-fit writes and connector arrowhead writes from the generator, regenerated the deck, opened every prefix from 1 to 21 slides through PowerPoint COM, then opened and resaved the final file through PowerPoint.
  - Final verification: PowerPoint COM opened the final file successfully with `21` slides.
  - Final SHA256: `800E8BE5EC19AD0EC936E8DC60EFCF610EEBFC28B44E36434892D6496C45C38F`.
- User requested a more accessible and more visual deck:
  - Increased core teaching text sizes for classroom projection and older students.
  - Restyled the deck with a warm beige editorial palette, subtle dot/line pattern accents, brown ink text, and cream cards.
  - Added generated bitmap visual assets under `docs/slides/assets/`: turbofan cutaway concept, AI workflow, uv environment, reference source board, PySide6 UI mockup, and bilingual report visual.
  - Regenerated the PPTX, opened it with PowerPoint COM, resaved it through PowerPoint, and re-opened the final file.
  - Final visual revision SHA256: `65BC15891C5DA4A8EFC390A682954013EC06F7732BB0F41E7C1FB58462CA996E`.
- `./scripts/verify-upstream-submodule.ps1`
  - Result: `Upstream submodule is clean and unchanged.`
- GitNexus `detect_changes` with `scope: all`
  - Result: risk level `low`, no affected processes. It reported tracked changes in `AGENTS.md` and `CLAUDE.md` for GitNexus index-count updates. New teaching assets are untracked document/binary assets and do not map to indexed execution flows.
- Final PowerPoint validation:
  - `uv run --with python-pptx python -c "from pptx import Presentation; ..."`
  - Result: `slides 21`, `pictures 7`.
  - PowerPoint COM open check result: `PowerPoint open check slides=21`.
- `git status --short`
  - Result: new teaching assets under `Reference_sources/`, `docs/slides/`, `docs/superpowers/`, `docs/sessions/`, `docs/research/`, plus `README.md`, `MEMORY.md`, and this dev-log entry. `AGENTS.md` and `CLAUDE.md` include GitNexus count updates.

## Risks / follow-up

- CFM International and Safran web pages were reachable through browser/search context but command-line downloads were blocked by Vercel / Cloudflare checks. The manifest records those URLs and download status.
- The generated deck is a planning and teaching deck, not yet the executable PySide6 application.
- The pyCycle high-bypass turbofan example should be used as a teaching approximation. It must not be described as a calibrated CFM56-7B engine deck.
- Follow-up implementation should create wrapper modules outside `upstream/pyCycle`, and should run GitNexus impact analysis before modifying any existing symbol.
