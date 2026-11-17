#!/usr/bin/env bats
# tests/shell/test_repo_root_location.bats — location-independent REPO_ROOT (#198)
#
# The fork's gate scripts (check-metadata-schema.sh, sod.sh, eod.sh, pre-pr.sh)
# computed REPO_ROOT as SCRIPT_DIR/../.., which only resolves correctly while
# the scripts live in the fork checkout (scripts/bash/). Once shipped into a
# consumer tree (.specify/scripts/bash/, the `specify init` layout), ../.. lands
# one level short at .specify — check-metadata-schema.sh then reads
# .specify/specs/metadata.json instead of specs/metadata.json (#198).
#
# The fix routes all four scripts through get_repo_root() from common.sh, which
# honors SPECIFY_INIT_DIR, walks up to the .specify marker, and falls back to
# the script location — independent of install depth.
#
# Hermetic: every test builds its own consumer-style project fixture under a
# mktemp dir and runs the scripts from a foreign cwd. pre-pr's external tools
# (uvx, uv) are stubbed so no network and no real test runs happen.

setup() {
    REPO_ROOT="$(cd "${BATS_TEST_DIRNAME}/../.." && pwd)"
    BASH_DIR="$REPO_ROOT/scripts/bash"

    FIX_TMP="$(mktemp -d)"
    PROJ="$FIX_TMP/project"
    FOREIGN="$FIX_TMP/foreign"
    INSTALL="$PROJ/.specify/scripts/bash"

    mkdir -p "$INSTALL" "$PROJ/specs" "$FOREIGN"

    # Ship the scripts under test into the consumer layout.
    for f in common.sh check-metadata-schema.sh sod.sh eod.sh pre-pr.sh; do
        cp "$BASH_DIR/$f" "$INSTALL/$f"
    done

    # Schema-valid fixture metadata (all 8 checks of check-metadata-schema.sh).
    cat > "$PROJ/specs/metadata.json" <<'JSON'
{
  "name": "bats-fixture-project",
  "project": "bats-fixture",
  "version": "1.0.0",
  "fork_version": "satware-v1.4.0+1",
  "visibility": "public",
  "conformance_level": "L1",
  "dependencies": {
    "upstream": [
      {
        "repo": "github/spec-kit",
        "forge": "github",
        "url": "https://github.com/github/spec-kit"
      }
    ]
  }
}
JSON

    # Stub the heavy external tools pre-pr.sh invokes (fail fast, no network).
    STUB_BIN="$FIX_TMP/bin"
    mkdir -p "$STUB_BIN"
    printf '#!/usr/bin/env bash\nexit 1\n' > "$STUB_BIN/uvx"
    printf '#!/usr/bin/env bash\nexit 1\n' > "$STUB_BIN/uv"
    chmod +x "$STUB_BIN/uvx" "$STUB_BIN/uv"

    unset SPECIFY_INIT_DIR || true
}

teardown() {
    rm -rf "$FIX_TMP"
}

@test "metadata-schema: validates installed project metadata from a foreign cwd" {
    cd "$FOREIGN"
    run bash "$INSTALL/check-metadata-schema.sh"
    [ "$status" -eq 0 ]
    [[ "$output" == *"structurally valid"* ]]
}

@test "metadata-schema: names the project-root metadata path when unreadable" {
    rm "$PROJ/specs/metadata.json"
    cd "$FOREIGN"
    run bash "$INSTALL/check-metadata-schema.sh"
    [ "$status" -eq 2 ]
    [[ "$output" == *"$PROJ/specs/metadata.json"* ]]
    [[ "$output" != *".specify/specs/metadata.json"* ]]
}

@test "sod: reports the project root (not .specify) from a foreign cwd" {
    # Gate scripts are absent in the fixture layout, so sod.sh ends with
    # fail=1 (privacy FAILED, upstream-sync non-fatal) — exit 1 is expected.
    cd "$FOREIGN"
    HARNESS_DIR="/nonexistent/harness/path" run bash "$INSTALL/sod.sh"
    [[ "$output" == *"Repo: $PROJ"$* || "$output" == *"Repo: $PROJ"* ]]
    [[ "$output" != *"Repo: $PROJ/.specify"* ]]
    [ "$status" -eq 1 ]
}

@test "eod: reports the project root (not .specify) from a foreign cwd" {
    cd "$FOREIGN"
    HARNESS_DIR="/nonexistent/harness/path" run bash "$INSTALL/eod.sh"
    [[ "$output" == *"Repo: $PROJ"* ]]
    [[ "$output" != *"Repo: $PROJ/.specify"* ]]
    [ "$status" -eq 1 ]
}

@test "pre-pr: reports the project root and resolves chained gates from a foreign cwd" {
    # Gates after [2/6] reference $REPO_ROOT/scripts/bash/*, which do not exist
    # in the fixture — except check-metadata-schema.sh, which must resolve the
    # fixture project root and PASS. SATWARE_HARNESS is emptied to skip the
    # provenance step.
    cd "$FOREIGN"
    PATH="$STUB_BIN:$PATH" SATWARE_HARNESS="" HARNESS_DIR="/nonexistent/harness/path" \
        run bash "$INSTALL/pre-pr.sh"
    [[ "$output" == *"Repo: $PROJ"* ]]
    [[ "$output" != *"Repo: $PROJ/.specify"* ]]
    [[ "$output" == *"metadata schema passed"* ]]
    [ "$status" -eq 1 ]
}

@test "metadata-schema: SPECIFY_INIT_DIR override wins from a foreign cwd" {
    cd "$FOREIGN"
    SPECIFY_INIT_DIR="$PROJ" run bash "$INSTALL/check-metadata-schema.sh"
    [ "$status" -eq 0 ]
    [[ "$output" == *"structurally valid"* ]]
}

@test "regression: fork checkout layout still resolves the fork root" {
    cd "$REPO_ROOT"
    run bash "$BASH_DIR/check-metadata-schema.sh"
    [ "$status" -eq 0 ]
    [[ "$output" == *"structurally valid"* ]]
}
