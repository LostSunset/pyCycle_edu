# Developer Log Rules

Every developer and coding agent must keep a development log for meaningful repository work.

## When to write an entry

Create or update a log entry when you:

- analyze the codebase,
- change code, docs, configuration, or repository policy,
- update dependencies or tooling,
- run verification that affects a decision,
- discover an important constraint or risk.

Tiny read-only checks do not require a new entry unless they change the direction of the work.

## File naming

Use this format:

```text
docs/dev-log/YYYY-MM-DD-short-topic.md
```

Use the local project date. Keep the short topic lowercase and hyphenated.

## Required sections

Each entry must include:

- `Context`: why the work happened.
- `GitNexus analysis`: exact command used and a short result summary.
- `Changes`: files or settings changed.
- `Verification`: commands run and outcomes.
- `Risks / follow-up`: unresolved risks, TODOs, or `None`.

Start from `docs/dev-log/TEMPLATE.md`.

## GitNexus rule

Before code analysis or edits, run:

```powershell
npx gitnexus analyze --embeddings
```

If embeddings cannot be generated because credentials or network access are unavailable, record the failure and run:

```powershell
npx gitnexus analyze
```

Do not silently skip GitNexus analysis.

## Upstream submodule rule

`upstream/pyCycle` is a read-only reference to `https://github.com/OpenMDAO/pyCycle`.

Do not edit files inside the submodule and do not update the submodule pointer unless the owner explicitly requests an upstream sync. Before committing, run:

```powershell
./scripts/verify-upstream-submodule.ps1
```

