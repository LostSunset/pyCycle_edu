# 2026-05-13 README Tooling Prerequisites

## Context

- Added requested setup guidance for new contributors before they create the project virtual environment.

## Changes

- Updated `README.md` with installation commands and official download links for Git, GitHub CLI, uv, and Visual Studio Code Insiders.
- Clarified that Git/GitHub CLI setup, `gh auth login`, and uv-managed Python 3.12 `.venv` setup come before the existing project environment commands.
- Reworked `README.md` into a bilingual document with Traditional Chinese first by default and an English section reachable through the top language switch links.
- Added `docs/sessions/2026-05-13-readme-bilingual-tooling-session.md` to record version, release, changelog, governance-doc, and research-log decisions for this README-only update.

## Verification

- `Get-Content -Path README.md` — confirmed the README now opens with Traditional Chinese, includes top language switch links, and keeps the English section below.
- `rg -n "GitHub CLI|gh auth login|GitHub.cli|cli.github" README.md docs/dev-log/2026-05-13-readme-tooling-prereqs.md` — confirmed GitHub CLI install and login guidance is present.
- `gh --version`; `gh auth status` — confirmed GitHub CLI is installed and authenticated.
- `./scripts/verify-upstream-submodule.ps1` — confirmed upstream submodule is clean and unchanged.

## Risks / follow-up

- None.
