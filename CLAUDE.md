# Repository Instructions for Claude Code

This repository is the education/workspace wrapper for upstream pyCycle.

## Required workflow

1. Before analyzing or changing code, run GitNexus from the repository root:

   ```powershell
   npx gitnexus analyze --embeddings
   ```

   Use the generated GitNexus graph/vector context to understand symbol and file relationships before editing.

2. Do not modify the upstream submodule at `upstream/pyCycle`.

   - Treat it as read-only reference code.
   - Do not edit files inside it.
   - Do not update its gitlink pointer unless the repository owner explicitly asks for an upstream sync.
   - Before committing, run:

     ```powershell
     ./scripts/verify-upstream-submodule.ps1
     ```

3. Record every meaningful development task in `docs/dev-log/`.

   - Follow `docs/dev-log/README.md`.
   - Use `docs/dev-log/TEMPLATE.md` for new entries.
   - Include the GitNexus command/result used for analysis.
   - Mention any files changed and any verification commands run.

4. Work on feature branches and open pull requests for review.

   The repository owner/admin may push directly when needed. Other contributors should use PRs.

5. For every PPTX generated or modified under `docs/slides/`, export the deck to PNG preview images and visually inspect them before claiming completion.

   - Use `./docs/slides/export-pptx-preview.ps1`.
   - Check that text stays inside frames and is not clipped.
   - Check that images preserve aspect ratio and are not stretched.
   - Check classroom readability, including older students and projector viewing.
   - Mention the visual preview result in the dev log.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **pyCycle_edu** (3024 symbols, 4333 relationships, 37 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/pyCycle_edu/context` | Codebase overview, check index freshness |
| `gitnexus://repo/pyCycle_edu/clusters` | All functional areas |
| `gitnexus://repo/pyCycle_edu/processes` | All execution flows |
| `gitnexus://repo/pyCycle_edu/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
