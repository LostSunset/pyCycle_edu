# 2026-05-11 Initial Governance

## Context

- Initialized the public `LostSunset/pyCycle_edu` repository governance baseline.
- Added upstream `OpenMDAO/pyCycle` as a read-only reference remote and submodule.
- Added rules so Claude Code and Codex agents record development logs consistently.

## GitNexus analysis

- Command: `npx gitnexus analyze --embeddings`
- Result: Repository indexed successfully in 504.5s. GitNexus reported 2,423 nodes, 3,419 edges, 51 clusters, and 15 flows. It also reported that semantic embeddings were generated without a VECTOR index, so queries will use exact-scan fallback within the configured limit.

## Changes

- Added `AGENTS.md` for Codex instructions.
- Added `CLAUDE.md` for Claude Code instructions.
- Added developer log rules and template under `docs/dev-log/`.
- Added `scripts/verify-upstream-submodule.ps1` to detect upstream submodule edits or gitlink changes.
- Added `upstream/pyCycle` as the read-only upstream submodule.

## Verification

- `npx gitnexus analyze --embeddings`: completed successfully.
- `npx gitnexus status`: index is up to date.
- Pending until after initial commit/push:
  - `./scripts/verify-upstream-submodule.ps1`
  - `git status --short`
  - `gh api` branch protection readback after push

## Risks / follow-up

- GitHub branch protection can only be applied after the initial `main` branch exists on GitHub.
- The initial commit intentionally adds the `upstream/pyCycle` submodule pointer because the owner requested the upstream reference. Future commits must not modify that submodule or pointer unless the owner explicitly requests an upstream sync.
