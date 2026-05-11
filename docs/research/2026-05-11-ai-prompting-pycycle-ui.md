# 2026-05-11 Research Goal and Log

## Research / Teaching Goal

Develop a student-facing workflow that teaches AI prompting for engineering computation:

1. Use `uv` to create reproducible Python environments.
2. Use pyCycle as a gas turbine cycle modeling reference.
3. Use public CFM56-7B-class data for first-pass validation literacy.
4. Build toward a PySide6 UI that presents GasTurb-like entry-level workflows.
5. Generate Traditional Chinese and English engineering reports with source citations and model limitations.

## Current Scope

- Teaching plan and PPT only.
- No pyCycle wrapper code has been implemented yet.
- No PySide6 application has been implemented yet.
- External source governance and manifest have been started.

## Current Result

- A 21-slide Traditional Chinese PPT has been generated at `docs/slides/pycycle_ai_prompting_course.pptx`.
- The deck includes larger text for classroom projection and older students.
- The deck includes generated bitmap visuals for the turbofan concept, AI workflow, uv environment, source governance, PySide6 UI mockup, and bilingual reports.
- PPTX generation now requires PNG preview export and visual inspection so text overflow, clipped text, and distorted images are caught before completion.

## Validation Notes

- The final PPTX was opened through Microsoft PowerPoint COM and resaved successfully.
- The final PPTX contains 7 embedded pictures.
- The upstream pyCycle submodule was verified clean and unchanged.
- Preview PNGs are exported with `docs/slides/export-pptx-preview.ps1` and should be visually reviewed for classroom readability.

## Open Research Questions

- Which CFM56-7B variant should be the first quantitative comparison target?
- Which public fields are reliable enough for numerical validation rather than qualitative comparison?
- How much of GasTurb's workflow should be approximated in the first PySide6 UI milestone?
- Should reports be Markdown-first, PDF-first, or both?

## Next Milestone

Create an executable teaching skeleton:

- `pyproject.toml` managed by `uv`,
- wrapper module outside `upstream/pyCycle`,
- command to run the pyCycle high-bypass turbofan example,
- CSV/Markdown summary output,
- minimal PySide6 window that displays inputs and outputs.
