# Shell tests (bats-core)

IPADP Phase 4.2 (issue #23) — automated tests for the fork's bash scripts.

## Coverage

| Script | Test file |
|---|---|
| `scripts/daily-routine.sh` | `test_daily_routine.bats` |
| `scripts/bash/sod.sh` | `test_sod.bats` |
| `scripts/bash/eod.sh` | `test_eod.bats` |
| `scripts/bash/check-privacy-leaks.sh` | `test_check_privacy_leaks.bats` |
| `scripts/bash/check-upstream-sync.sh` | `test_check_upstream_sync.bats` |

Each file provides at least two positive and one negative test.

## Running locally

```bash
# Ubuntu / Debian
sudo apt-get install -y bats

# macOS
brew install bats-core

# From repo root
bats tests/shell/
```

## CI

Run on every push and PR via `.github/workflows/shell-tests.yml` (ubuntu-latest).

## Fallback paths exercised

- `CLINE_DIR` pointing to a missing directory → SoD/EoD must still exit 0 with a warning.
- Missing `upstream` remote → `check-upstream-sync.sh` must fail gracefully (non-zero, with a meaningful message).
