#!/usr/bin/env bats
# tests/shell/test_eod.bats — IPADP Phase 4.2 (issue #23)
# Covers scripts/bash/eod.sh.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    EOD="$REPO_ROOT/scripts/bash/eod.sh"
}

@test "eod: runs and exits 0 on clean tree with Cline stack missing" {
    CLINE_DIR="/nonexistent/cline/path" run "$EOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"End-of-Day"* ]]
    [[ "$output" == *"Cline stack not found"* ]]
}

@test "eod: invokes privacy check" {
    CLINE_DIR="/nonexistent/cline/path" run "$EOD"
    [ "$status" -eq 0 ]
    [[ "$output" == *"privacy leak check"* ]]
    [[ "$output" == *"privacy check passed"* ]]
}

@test "eod: references Cline protocol when stack is present" {
    tmpdir="$(mktemp -d)"
    mkdir -p "$tmpdir/Workflows"
    printf '# EoD protocol stub\n' > "$tmpdir/Workflows/eod.protocol.md"
    CLINE_DIR="$tmpdir" run "$EOD"
    rm -rf "$tmpdir"
    [ "$status" -eq 0 ]
    [[ "$output" == *"Cline EoD protocol:"* ]]
    [[ "$output" == *"eod.protocol.md"* ]]
}
