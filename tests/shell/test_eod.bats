#!/usr/bin/env bats
# tests/shell/test_eod.bats — IPADP Phase 4.2 (issue #23)
# Covers scripts/bash/eod.sh.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    EOD="$REPO_ROOT/scripts/bash/eod.sh"
}

@test "eod: runs and exits 0 on clean tree with harness missing" {
    HARNESS_DIR="/nonexistent/harness/path" run "$EOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"End-of-Day"* ]]
    [[ "$output" == *"Harness not found"* ]]
}

@test "eod: invokes privacy check" {
    HARNESS_DIR="/nonexistent/harness/path" run "$EOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"privacy leak check"* ]]
    [[ "$output" == *"privacy check passed"* ]]
}

@test "eod: references harness protocol when harness is present" {
    tmpdir="$(mktemp -d)"
    mkdir -p "$tmpdir/workflows"
    printf '# EoD protocol stub\n' > "$tmpdir/workflows/eod.protocol.md"
    HARNESS_DIR="$tmpdir" run "$EOD"
    rm -rf "$tmpdir"
    [ "$status" -eq 0 ]
    [[ "$output" == *"EoD protocol:"* ]]
    [[ "$output" == *"eod.protocol.md"* ]]
}
