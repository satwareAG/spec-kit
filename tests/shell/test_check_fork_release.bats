#!/usr/bin/env bats
# tests/shell/test_check_fork_release.bats — fork release guard (issue #131)
#
# Hermetic: every test builds its own git repo and stubs `gh`, so no network
# and no forge writes are required.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    CHECK="$REPO_ROOT/scripts/bash/check-fork-release.sh"

    TEST_TMP="$(mktemp -d)"
    GH_LOG="$TEST_TMP/gh.log"
    mkdir -p "$TEST_TMP/bin"
    cat > "$TEST_TMP/bin/gh" <<'STUB'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "${GH_LOG:?}"
if [[ "${STUB_RELEASE_PRESENT:-0}" == "1" ]]; then
    exit 0
fi
echo "release not found" >&2
exit 1
STUB
    chmod +x "$TEST_TMP/bin/gh"
    export GH="$TEST_TMP/bin/gh"
    export GH_LOG
}

teardown() {
    rm -rf "$TEST_TMP"
}

# make_repo <dir> [fork_tag] — git repo whose HEAD has upstream tag v1.0.0
# merged; optionally carrying a fork tag `satware-v1.0.0+1`.
make_repo() {
    local dir="$1"
    local fork_tag="${2:-}"
    git init -q "$dir"
    (
        cd "$dir"
        git config user.email bats@example.com
        git config user.name bats
        git commit --allow-empty -q -m init
        git tag v1.0.0
        if [[ -n "$fork_tag" ]]; then
            git tag "$fork_tag"
        fi
    )
}

@test "fork-release: --help exits 0 and prints usage" {
    run "$CHECK" --help
    [ "$status" -eq 0 ]
    [[ "$output" == *"Usage:"* ]]
    [[ "$output" == *"--json"* ]]
}

@test "fork-release: repo with no upstream tag passes as no-upstream-tag" {
    local repo="$TEST_TMP/noup"
    git init -q "$repo"
    (cd "$repo" && git config user.email bats@example.com && git config user.name bats \
        && git commit --allow-empty -q -m init && git tag satware-v9.9.9+1)

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --json
    [ "$status" -eq 0 ]
    [[ "$output" == *'"status":"no-upstream-tag"'* ]]
    [[ "$output" == *'"ok":true'* ]]
}

@test "fork-release: missing fork tag fails the guard (v1.0.7 regression case)" {
    local repo="$TEST_TMP/missing"
    make_repo "$repo"

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --json
    [ "$status" -eq 1 ]
    [[ "$output" == *'"ok":false'* ]]
    [[ "$output" == *'"status":"missing"'* ]]
    [[ "$output" == *'"upstream_tag":"v1.0.0"'* ]]
    [[ "$output" == *'"expected_fork_tag":"satware-v1.0.0+1"'* ]]
    [[ "$output" == *'"tag_present":false'* ]]
    [[ "$output" == *'"release_present":false'* ]]
}

@test "fork-release: tag present but release missing fails the guard" {
    local repo="$TEST_TMP/norel"
    make_repo "$repo" "satware-v1.0.0+1"
    export STUB_RELEASE_PRESENT=0

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --json
    [ "$status" -eq 1 ]
    [[ "$output" == *'"tag_present":true'* ]]
    [[ "$output" == *'"release_present":false'* ]]
}

@test "fork-release: tag and release present passes" {
    local repo="$TEST_TMP/ok"
    make_repo "$repo" "satware-v1.0.0+1"
    export STUB_RELEASE_PRESENT=1

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --json
    [ "$status" -eq 0 ]
    [[ "$output" == *'"ok":true'* ]]
    [[ "$output" == *'"status":"ok"'* ]]
    [[ "$output" == *'"tag_present":true'* ]]
    [[ "$output" == *'"release_present":true'* ]]
}

@test "fork-release: derives owner/repo from an https origin remote" {
    local repo="$TEST_TMP/slug"
    make_repo "$repo"
    (cd "$repo" && git remote add origin https://github.com/owner/repo.git)
    export STUB_RELEASE_PRESENT=1

    run "$CHECK" --repo "$repo" --json
    [ "$status" -ne 2 ]
    grep -q -- "--repo owner/repo" "$GH_LOG"
}

@test "fork-release: derives owner/repo from an scp-style origin remote" {
    local repo="$TEST_TMP/slug-ssh"
    make_repo "$repo"
    (cd "$repo" && git remote add origin git@github.com:owner/repo.git)
    export STUB_RELEASE_PRESENT=1

    run "$CHECK" --repo "$repo" --json
    [ "$status" -ne 2 ]
    grep -q -- "--repo owner/repo" "$GH_LOG"
}

@test "fork-release: unknown ref exits 2 as an environment error" {
    local repo="$TEST_TMP/badref"
    make_repo "$repo" "satware-v1.0.0+1"

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --ref does-not-exist --json
    [ "$status" -eq 2 ]
    [[ "$output" == *'"status":"error"'* ]]
}

@test "fork-release: missing gh exits 2 (fail closed)" {
    local repo="$TEST_TMP/nogh"
    make_repo "$repo" "satware-v1.0.0+1"
    export GH="$TEST_TMP/bin/does-not-exist"

    run "$CHECK" --repo "$repo" --repo-slug owner/repo --json
    [ "$status" -eq 2 ]
    [[ "$output" == *'"status":"error"'* ]]
}
