#!/usr/bin/env bats
# tests/shell/test_check_upstream_sync.bats — IPADP Phase 4.2 (issue #23)

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    CHECK="$REPO_ROOT/scripts/bash/check-upstream-sync.sh"
}

@test "upstream-sync: --help exits 0 and prints usage" {
    run "$CHECK" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Usage:"* ]]
    [[ "$output" == *"--json"* ]]
}

@test "upstream-sync: runs on repo (has upstream remote)" {
    # Repo has upstream configured; tolerate 0 (success) or network/other
    # non-zero, but must at least produce output or a known error.
    cd "$REPO_ROOT"
    run "$CHECK"
    # Either success or a controlled error — never a silent crash (127/139).
    [ "$status" -ne 127 ]
    [ "$status" -ne 139 ]
}

@test "upstream-sync: fails gracefully without upstream remote" {
    tmpdir="$(mktemp -d)"
    (
        cd "$tmpdir"
        git init -q
        git config user.email bats@example.com
        git config user.name bats
        git commit --allow-empty -q -m init
    )
    cd "$tmpdir"
    run "$CHECK"
    rm -rf "$tmpdir"
    [ "$status" -ne 0 ]
    [[ "$output" == *"upstream"* ]] || [[ "$output" == *"remote"* ]]
}
