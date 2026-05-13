# 2026-05-13 README om-pycycle Install

## Context

- User asked to add README guidance for installing `om-pycycle` with `uv`.

## Changes

- Updated `README.md` in both Traditional Chinese and English setup sections with `uv pip install om-pycycle`.

## Verification

- `rg -n "uv venv|uv sync|PySide6|om-pycycle|Environment|環境" README.md` — found the existing environment setup commands before editing.
- `./scripts/verify-upstream-submodule.ps1` — confirmed upstream submodule is clean and unchanged.

## Risks / follow-up

- None.
