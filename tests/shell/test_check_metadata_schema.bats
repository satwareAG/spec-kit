#!/usr/bin/env bats
# Structural validation gate for specs/metadata.json (#167).
# Positive control: the real metadata passes.
# Negative controls: each shape violation is caught (never silently accepted).

setup() {
  REPO_ROOT="$(cd "$BATS_TEST_DIRNAME/../.." && pwd)"
  SCRIPT="$REPO_ROOT/scripts/bash/check-metadata-schema.sh"
  TMP="$(mktemp -d)"
  cp "$REPO_ROOT/specs/metadata.json" "$TMP/metadata.json"
}

teardown() {
  rm -rf "$TMP"
}

# Run the validator against a modified copy by pointing it at a temp project.
run_against() {
  # The validator resolves METADATA via get_repo_root (#198): SPECIFY_INIT_DIR
  # wins, then the .specify marker walk from cwd, then script location. Point
  # it at the fixture project explicitly - the fixture is a standalone
  # spec-kit project layout (specs/ + .specify/ marker), not a copy of the
  # checkout's scripts tree.
  mkdir -p "$TMP/specs" "$TMP/.specify"
  cp "$TMP/metadata.json" "$TMP/specs/metadata.json"
  SPECIFY_INIT_DIR="$TMP" run bash "$SCRIPT"
}

@test "positive: real specs/metadata.json passes" {
  run bash "$SCRIPT"
  [ "$status" -eq 0 ]
}

@test "negative: invalid JSON is rejected" {
  echo '{ broken' > "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
}

@test "negative: missing fork_version is rejected" {
  jq 'del(.fork_version)' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"missing required key: fork_version"* ]]
}

@test "negative: malformed version is rejected" {
  jq '.version = "1.2"' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"version must be a semver triplet"* ]]
}

@test "negative: malformed fork_version is rejected" {
  jq '.fork_version = "satware-v1.2.6"' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"fork_version must match satware-vX.Y.Z+1"* ]]
}

@test "negative: bad conformance level is rejected" {
  jq '.conformance_level = "L9"' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"conformance_level must be L1, L2, or L3"* ]]
}

@test "negative: empty upstream array is rejected" {
  jq '.dependencies.upstream = []' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"dependencies.upstream must be a non-empty array"* ]]
}

@test "negative: typed downstream[] on public repo is rejected (#168 backstop)" {
  jq '.dependencies.downstream = [{"repo": "example/private", "forge": "gitea", "visibility": "private"}]' \
    "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"public repo must not carry typed dependencies.downstream[]"* ]]
}

@test "positive: anonymous downstream note passes" {
  jq '.dependencies.downstream = {note: "withheld"}' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -eq 0 ]
}

@test "negative: downstream object without note is rejected" {
  jq '.dependencies.downstream = {"internal": true}' "$TMP/metadata.json" > "$TMP/edited" && mv "$TMP/edited" "$TMP/metadata.json"
  run_against
  [ "$status" -ne 0 ]
  [[ "$output" == *"missing its anonymous rationale note"* ]]
}
