#!/usr/bin/env bats
# tests/shell/test_check_privacy_leaks.bats — IPADP Phase 4.2 (issue #23)

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    CHECK="$REPO_ROOT/scripts/bash/check-privacy-leaks.sh"
}

@test "privacy: passes on repo root (clean tree)" {
    run "$CHECK" "$REPO_ROOT"
    [ "$status" -eq 0 ]
    [[ "$output" == *"No privacy violations"* ]]
}

@test "privacy: passes on empty tmp repo" {
    tmpdir="$(mktemp -d)"
    (
        cd "$tmpdir"
        git init -q
        git config user.email bats@example.com
        git config user.name bats
        git commit --allow-empty -q -m init
    )
    run "$CHECK" "$tmpdir"
    rm -rf "$tmpdir"
    [ "$status" -eq 0 ]
}

@test "privacy: fails when private URL is present" {
    tmpdir="$(mktemp -d)"
    (
        cd "$tmpdir"
        git init -q
        git config user.email bats@example.com
        git config user.name bats
        printf 'see https://gitlab.satware.com/foo\n' > leak.md
        git add leak.md
        git commit -q -m "leak"
    )
    run "$CHECK" "$tmpdir"
    rm -rf "$tmpdir"
    [ "$status" -ne 0 ]
    [[ "$output" == *"gitlab.satware.com"* ]] || [[ "$output" == *"Private GitLab URL"* ]]
}
