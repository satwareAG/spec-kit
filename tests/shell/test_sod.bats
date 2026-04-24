#!/usr/bin/env bats
# tests/shell/test_sod.bats — IPADP Phase 4.2 (issue #23)
# Covers scripts/bash/sod.sh.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    SOD="$REPO_ROOT/scripts/bash/sod.sh"
}

@test "sod: runs and exits 0 on clean tree with Cline stack missing" {
    # Force Cline stack missing to exercise the fallback path.
    CLINE_DIR="/nonexistent/cline/path" run "$SOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Start-of-Day"* ]]
    [[ "$output" == *"Cline stack not found"* ]]
}

@test "sod: invokes privacy + upstream-sync checks" {
    CLINE_DIR="/nonexistent/cline/path" run "$SOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"privacy leak check"* ]]
    [[ "$output" == *"upstream sync check"* ]]
}

@test "sod: references Cline protocol when stack is present" {
    tmpdir="$(mktemp -d)"
    mkdir -p "$tmpdir/Workflows"
    printf '# SoD protocol stub\n' > "$tmpdir/Workflows/sod.protocol.md"
    CLINE_DIR="$tmpdir" run "$SOD"
    rm -rf "$tmpdir"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Cline SoD protocol:"* ]]
    [[ "$output" == *"sod.protocol.md"* ]]
}
