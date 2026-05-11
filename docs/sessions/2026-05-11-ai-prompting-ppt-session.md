# 2026-05-11 AI Prompting PPT Session

## Summary

- Planned and generated a Traditional Chinese teaching PPT for AI prompting, uv environment management, pyCycle validation, and PySide6 UI planning.
- Selected CFM56-7B-class high-bypass turbofan as the first teaching case.
- Stored reference-source rules and available source files under `Reference_sources/`.
- Reworked the PPT after user feedback to use larger classroom-friendly text, a warm beige visual style, and embedded bitmap illustrations.

## Key Decisions

- `upstream/pyCycle` remains read-only.
- pyCycle's `high_bypass_turbofan.py` is used as a learning scaffold, not a calibrated CFM56-7B engine deck.
- This work is documentation/teaching material, not a package version bump.
- No GitHub Release is required until the repository has a version/tag policy.

## Important Files

- `README.md`
- `MEMORY.md`
- `Reference_sources/README.md`
- `Reference_sources/source_manifest.md`
- `docs/slides/build_pycycle_ai_prompting_ppt.py`
- `docs/slides/pycycle_ai_prompting_course.pptx`
- `docs/slides/assets/`
- `docs/dev-log/2026-05-11-pycycle-ai-prompting-ppt.md`
- `docs/research/2026-05-11-ai-prompting-pycycle-ui.md`

## Verification Snapshot

- GitNexus: `npx gitnexus analyze --embeddings` reported the index was up to date during finalization.
- PowerPoint COM opened the final PPTX successfully with 21 slides.
- PPTX contains 7 embedded pictures.
- Upstream submodule check reported clean and unchanged.

## Follow-up

- Implement the first executable teaching milestone: `uv` project setup plus a wrapper that runs the high-bypass turbofan example without editing upstream.
- Add a versioning/release policy before publishing GitHub Releases.

