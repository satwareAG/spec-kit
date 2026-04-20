# IPADP L3 Upstream Sync Automation

This document describes the L3 automation layer of the Inter-Project Agentic
Development Process (IPADP) on the `satwareAG/spec-kit` fork. It ties together
the scheduled upstream-sync CI workflow and the repo-local Start-of-Day / End-of-Day
(SoD/EoD) protocol hooks so agents and maintainers can keep the fork continuously
aligned with upstream `github/spec-kit` while preserving fork-only agent support.

See also:
- `AGENTS.md` — IPADP Conformance & Cline Harmony section (L1/L2/L3 matrix).
- `specs/metadata.json` — machine-readable project + IPADP metadata.
- Internal IPADP RFC in the satware AG `wiki` repo
  (`specs/rfc-interproject-agentic-development.md`).

## 1. Scheduled upstream-sync CI workflow

**File:** `.github/workflows/upstream-sync-check.yml`

### Purpose

Detect new upstream `github/spec-kit` release tags and surface them as a single,
idempotent tracking issue on the fork so the maintainer can plan the next sync.

### Triggers

- `schedule` — daily cron.
- `workflow_dispatch` — manual run from the Actions tab.

### Behavior

1. Checks out the fork with full history and tags (both origin and upstream).
2. Runs `scripts/bash/check-upstream-sync.sh --json` to compute the latest
   upstream release tag and whether the current fork tip is already synced.
3. If a newer upstream tag is available, creates or updates exactly one
   rolling issue titled `upstream-sync: <tag> available` labeled
   `upstream-sync` + `enhancement`. Re-runs without a new tag produce no issue
   churn (idempotent).
4. Uses only `GITHUB_TOKEN` — no extra secrets required.

### Manual run

```bash
gh workflow run upstream-sync-check.yml --repo satwareAG/spec-kit
```

### Failure modes / overrides

- If upstream is unreachable, the workflow exits non-zero and the run is
  visible in the Actions tab — no issue is created.
- Rolling issue can be closed manually once the sync PR has landed; the
  workflow will re-open/update it only when a *newer* upstream tag appears.

## 2. Repo-local SoD / EoD hooks

**Files:** `scripts/bash/sod.sh`, `scripts/bash/eod.sh`, `scripts/daily-routine.sh`.

### Purpose

Run the canonical satware AG daily rituals (Start-of-Day / End-of-Day protocols
from `~/Documents/Cline/Workflows/`) locally on the repo and tie them to the
two validation checks the fork must honor: privacy + upstream sync.

### Start-of-Day (`sod`)

```bash
bash scripts/daily-routine.sh sod
```

1. References `~/Documents/Cline/Workflows/sod.protocol.md` (graceful
   non-fatal fallback with a warning if the Cline stack is absent).
2. Runs `scripts/bash/check-privacy-leaks.sh .`.
3. Runs `scripts/bash/check-upstream-sync.sh`.

### End-of-Day (`eod`)

```bash
bash scripts/daily-routine.sh eod
```

1. References `~/Documents/Cline/Workflows/eod.protocol.md` (graceful fallback).
2. Runs `scripts/bash/check-privacy-leaks.sh .`.

### Dispatcher

`scripts/daily-routine.sh` accepts `sod`, `eod`, and `help` subcommands and is
safe to run from any CWD inside the repo.

## 3. Local run instructions

```bash
# Sanity checks
bash scripts/daily-routine.sh help
bash scripts/daily-routine.sh sod
bash scripts/daily-routine.sh eod

# Underlying checks directly
bash scripts/bash/check-privacy-leaks.sh .
bash scripts/bash/check-upstream-sync.sh
bash scripts/bash/check-upstream-sync.sh --json
```

## 4. Failure modes and manual override

| Condition | Effect | Manual override |
|---|---|---|
| `~/Documents/Cline/` absent | Hooks warn and continue (non-fatal). | Clone/symlink the Cline stack per `AGENTS.md` Harmony section. |
| `upstream` remote missing | `check-upstream-sync.sh` exits non-zero. | `git remote add upstream https://github.com/github/spec-kit` then `git fetch upstream --tags`. |
| Privacy violation detected | SoD/EoD hook fails; CI `privacy-check` workflow blocks merge. | Fix the leak or extend `.privacy-whitelist` with justification. |
| Rolling upstream-sync issue obsolete | Close it manually. | The scheduled workflow re-creates/updates the issue only on a strictly newer upstream tag. |

## 5. Conformance

These artifacts satisfy the L3 row of the IPADP conformance matrix in
`AGENTS.md`: automated upstream sync detection plus morning-protocol integration.
Combined with L1 (`AGENTS.md` + `specs/metadata.json`) and L2 (privacy validation
in CI), the fork reaches full IPADP L3 conformance as project #6.
