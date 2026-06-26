#!/usr/bin/env bats
# tests/shell/test_sod.bats — IPADP Phase 4.2 (issue #23)
# Covers scripts/bash/sod.sh.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    SOD="$REPO_ROOT/scripts/bash/sod.sh"
}

@test "sod: runs and exits 0 on clean tree with harness missing" {
    # Force harness missing to exercise the fallback path.
    HARNESS_DIR="/nonexistent/harness/path" run "$SOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Start-of-Day"* ]]
    [[ "$output" == *"Harness not found"* ]]
}

@test "sod: invokes privacy + upstream-sync checks" {
    HARNESS_DIR="/nonexistent/harness/path" run "$SOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"privacy leak check"* ]]
    [[ "$output" == *"upstream sync check"* ]]
}

@test "sod: references harness protocol when harness is present" {
    tmpdir="$(mktemp -d)"
    mkdir -p "$tmpdir/workflows"
    printf '# SoD protocol stub\n' > "$tmpdir/workflows/sod.protocol.md"
    HARNESS_DIR="$tmpdir" run "$SOD"
    rm -rf "$tmpdir"
    [ "$status" -eq 0 ]
    [[ "$output" == *"SoD protocol:"* ]]
    [[ "$output" == *"sod.protocol.md"* ]]
}
