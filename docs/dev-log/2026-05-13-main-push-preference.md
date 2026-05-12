# 2026-05-13 Main Push Preference

## Context

- User asked to remember that future commit/push work should go directly to `main`.

## Changes

- Updated `MEMORY.md` with the user's preference to push repository work directly to `main` when asked to commit/push, while still respecting repository safety checks.

## Verification

- `git status -sb` — confirmed the workspace state before editing.
- `./scripts/verify-upstream-submodule.ps1` — confirmed upstream submodule is clean and unchanged.

## Risks / follow-up

- This preference is constrained by repository safety checks and explicit user requests.
