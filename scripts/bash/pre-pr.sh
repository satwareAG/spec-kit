#!/usr/bin/env bash
# pre-pr.sh — local health check to run before pushing a PR (IPADP Phase 4.5).
#
# Runs the same validation suite that CI enforces, so failures are caught
# locally before spending a CI run.  Fail-fast: any step failure aborts
# immediately with a non-zero exit code.
#
# Exit codes:
#   0  all checks passed
#   1  one or more checks failed

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== pre-pr: spec-kit local health check ==="
echo "Repo: $REPO_ROOT"
date

fail=0

# 1. Ruff lint (matches CI: uvx ruff check src/)
echo ""
echo "[1/4] ruff check src/..."
if uvx --from "ruff>=0.14" ruff check "$REPO_ROOT/src/"; then
    echo "   ruff passed"
else
    echo "   ruff FAILED"
    fail=1
fi

# 2. Integration tests (stop on first failure, quiet)
echo ""
echo "[2/4] pytest tests/integrations/ ..."
if (cd "$REPO_ROOT" && uv run pytest tests/integrations/ -x -q --no-header); then
    echo "   tests passed"
else
    echo "   tests FAILED"
    fail=1
fi

# 3. Privacy leak check
echo ""
echo "[3/4] check-privacy-leaks.sh..."
if "$REPO_ROOT/scripts/bash/check-privacy-leaks.sh" "$REPO_ROOT"; then
    echo "   privacy check passed"
else
    echo "   privacy check FAILED"
    fail=1
fi

# 4. Upstream sync check
echo ""
echo "[4/4] check-upstream-sync.sh..."
if "$REPO_ROOT/scripts/bash/check-upstream-sync.sh"; then
    echo "   upstream-sync check completed"
else
    echo "   upstream-sync check reported issues (non-fatal)"
    # Non-fatal: upstream sync warnings don't block PRs
fi

echo ""
if [ "$fail" -eq 0 ]; then
    echo "=== pre-pr: all checks passed ==="
else
    echo "=== pre-pr: failures detected - fix before pushing ==="
fi
exit "$fail"
