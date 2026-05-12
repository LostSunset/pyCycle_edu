# Repository Instructions for Codex

This repository is the education/workspace wrapper for upstream pyCycle.

**Current release: v0.2.0** — see `CHANGELOG.md`. The active end-user
deliverable is the standalone simple turbojet tutorial at
`tutorials/simple_turbojet/simple_turbojet.py` (PySide6 GUI + bilingual
user guide at `tutorials/simple_turbojet/README.md`). All tutorial outputs
land in `tutorials/simple_turbojet/output/` (gitignored).

## Required workflow

1. Do not modify the upstream submodule at `upstream/pyCycle`.

   - Treat it as read-only reference code.
   - Do not edit files inside it.
   - Do not update its gitlink pointer unless the repository owner explicitly asks for an upstream sync.
   - Before committing, run:

     ```powershell
     ./scripts/verify-upstream-submodule.ps1
     ```

2. Record every meaningful development task in `docs/dev-log/`.

   - Follow `docs/dev-log/README.md`.
   - Use `docs/dev-log/TEMPLATE.md` for new entries.
   - Mention any files changed and any verification commands run.

3. Work on feature branches and open pull requests for review.

   The repository owner/admin may push directly when needed. Other contributors should use PRs.

4. For every PPTX generated or modified under `docs/slides/`, export the deck to PNG preview images and visually inspect them before claiming completion.

   - Use `./docs/slides/export-pptx-preview.ps1`.
   - Check that text stays inside frames and is not clipped.
   - Check that images preserve aspect ratio and are not stretched.
   - Check classroom readability, including older students and projector viewing.
   - Mention the visual preview result in the dev log.
