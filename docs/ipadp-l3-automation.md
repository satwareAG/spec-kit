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

**Files:** `scripts/bash/sod.sh`, `scripts/bash/eod.sh`, `scripts/bash/daily-routine.sh`.

### Purpose

Run the canonical satware AG daily rituals (Start-of-Day / End-of-Day protocols
from `~/Documents/Cline/Workflows/`) locally on the repo and tie them to the
two validation checks the fork must honor: privacy + upstream sync.

### Start-of-Day (`sod`)

```bash
bash scripts/bash/daily-routine.sh sod
```

1. References `~/Documents/Cline/Workflows/sod.protocol.md` (graceful
   non-fatal fallback with a warning if the Cline stack is absent).
2. Runs `scripts/bash/check-privacy-leaks.sh .`.
3. Runs `scripts/bash/check-upstream-sync.sh`.

### End-of-Day (`eod`)

```bash
bash scripts/bash/daily-routine.sh eod
```

1. References `~/Documents/Cline/Workflows/eod.protocol.md` (graceful fallback).
2. Runs `scripts/bash/check-privacy-leaks.sh .`.

### Dispatcher

`scripts/bash/daily-routine.sh` accepts `sod`, `eod`, and `help` subcommands and is
safe to run from any CWD inside the repo.

## 3. Local run instructions

```bash
# Sanity checks
bash scripts/bash/daily-routine.sh help
bash scripts/bash/daily-routine.sh sod
bash scripts/bash/daily-routine.sh eod

# Underlying checks directly
bash scripts/bash/check-privacy-leaks.sh .
bash scripts/bash/check-upstream-sync.sh
bash scripts/bash/check-upstream-sync.sh --json
bash scripts/bash/check-fork-release.sh --json
```

## 4. Fork release guard (#131)

**File:** `scripts/bash/check-fork-release.sh`, wired into
`.github/workflows/upstream-sync-check.yml` (daily + manual dispatch).

### Purpose

The sync procedure makes the fork release step mandatory (#112): every merged
upstream sync must cut `satware-vX.Y.Z+1` **and** publish a GitHub release
object. Nothing enforced it, and it was skipped for v1.0.7, v1.0.12 and
v1.1.2. The guard finds the newest upstream tag merged into the checked ref
and fails when the matching fork tag or release object is absent.

### Behavior

1. Runs after the upstream-sync detection step, checking out `main-speck`
   with full history and tags.
2. `check-fork-release.sh --json` reports
   `{ok, status, upstream_tag, expected_fork_tag, tag_present, release_present}`.
3. On a gap, the workflow opens/updates exactly one rolling issue titled
   `fork-release: satware-vX.Y.Z+1 missing` (label `fork-release`) carrying
   the backfill commands.
4. When the tag and release exist, the matching issue is closed
   automatically, so the thread cannot go stale.

### Backfill a missing release

Always publish backfills with `--latest=false`; otherwise an old tag hijacks
`releases/latest` and the CLI provenance chain resolves the wrong version.

```bash
gh release create satware-v1.1.2+1 --verify-tag --latest=false \
  --title "satware-v1.1.2+1 - upstream v1.1.2" --notes-file notes.md
```

### Exit codes

| Code | Meaning | Workflow effect |
|---|---|---|
| 0 | Fork tag and release present, or no upstream tag merged | Green |
| 1 | Merged upstream tag lacks a fork tag and/or release | Opens/updates the tracking issue |
| 2 | Environment/usage error (not a repo, unknown ref, `gh` missing) | Job fails, no issue written |

## 5. Failure modes and manual override

| Condition | Effect | Manual override |
|---|---|---|
| `~/Documents/Cline/` absent | Hooks warn and continue (non-fatal). | Clone/symlink the Cline stack per `AGENTS.md` Harmony section. |
| `upstream` remote missing | `check-upstream-sync.sh` exits non-zero. | `git remote add upstream https://github.com/github/spec-kit` then `git fetch upstream --tags`. |
| Privacy violation detected | SoD/EoD hook fails; CI `privacy-check` workflow blocks merge. | Fix the leak or extend `.privacy-whitelist` with justification. |
| Rolling upstream-sync issue obsolete | Close it manually. | The scheduled workflow re-creates/updates the issue only on a strictly newer upstream tag. |
| Fork release missing after a sync merge | Guard opens `fork-release: ... missing` and stays red. | Cut the tag, publish the release with `--latest=false`, re-run the guard. |

## 6. Conformance

These artifacts satisfy the L3 row of the IPADP conformance matrix in
`AGENTS.md`: automated upstream sync detection plus morning-protocol integration.
Combined with L1 (`AGENTS.md` + `specs/metadata.json`) and L2 (privacy validation
in CI), the fork reaches full IPADP L3 conformance as project #6.
