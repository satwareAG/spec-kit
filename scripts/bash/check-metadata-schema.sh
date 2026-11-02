#!/usr/bin/env bash
# check-metadata-schema.sh — structural validation of specs/metadata.json (#167).
#
# The IPADP metadata file drives SOD scans, release guards, and the fleet-wide
# W2/W3 validators; a malformed field silently breaks every consumer. This gate
# catches shape violations in the pre-pr chain BEFORE push, including the
# public-repo privacy shape rule (no typed downstream[] fan-out on a public
# repo - the regression class from #168).
#
# Exit codes:
#   0  metadata structurally valid
#   1  one or more violations (each printed as [FAIL] line)
#   2  jq missing or file unreadable (environment error)

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
METADATA="${REPO_ROOT}/specs/metadata.json"

if ! command -v jq >/dev/null 2>&1; then
  echo "[FAIL] jq not available - cannot validate metadata (install jq)"
  exit 2
fi

if [[ ! -r "${METADATA}" ]]; then
  echo "[FAIL] specs/metadata.json not found or unreadable: ${METADATA}"
  exit 2
fi

fail=0

fail_msg() {
  echo "[FAIL] metadata-schema: $*"
  fail=1
}

# 1. Valid JSON
if ! jq empty "${METADATA}" 2>/dev/null; then
  echo "[FAIL] metadata-schema: invalid JSON in specs/metadata.json"
  exit 1
fi

# 2. Required top-level keys
for key in name project version fork_version visibility conformance_level dependencies; do
  if ! jq -e --arg k "${key}" 'has($k)' "${METADATA}" >/dev/null; then
    fail_msg "missing required key: ${key}"
  fi
done

# 3. version: semver triplet
if ! jq -re '.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$")' "${METADATA}" >/dev/null 2>&1; then
  fail_msg "version must be a semver triplet (X.Y.Z), got: $(jq -r '.version // "null"' "${METADATA}")"
fi

# 4. fork_version: satware-vX.Y.Z+1
if ! jq -re '.fork_version | test("^satware-v[0-9]+\\.[0-9]+\\.[0-9]+\\+1$")' "${METADATA}" >/dev/null 2>&1; then
  fail_msg "fork_version must match satware-vX.Y.Z+1, got: $(jq -r '.fork_version // "null"' "${METADATA}")"
fi

# 5. conformance_level: L1|L2|L3
if ! jq -re '.conformance_level | test("^L[1-3]$")' "${METADATA}" >/dev/null 2>&1; then
  fail_msg "conformance_level must be L1, L2, or L3, got: $(jq -r '.conformance_level // "null"' "${METADATA}")"
fi

# 6. visibility: public|private
if ! jq -re '.visibility | test("^(public|private)$")' "${METADATA}" >/dev/null 2>&1; then
  fail_msg "visibility must be public or private, got: $(jq -r '.visibility // "null"' "${METADATA}")"
fi

# 7. dependencies.upstream: non-empty array, each entry typed
if ! jq -e '.dependencies.upstream | type == "array" and length > 0' "${METADATA}" >/dev/null 2>&1; then
  fail_msg "dependencies.upstream must be a non-empty array"
else
  if ! jq -e 'all(.dependencies.upstream[]; has("repo") and has("forge") and has("url"))' "${METADATA}" >/dev/null 2>&1; then
    fail_msg "every dependencies.upstream entry needs repo, forge, url"
  fi
fi

# 8. Public-repo privacy shape (#168 backstop): a public repo MUST NOT carry a
#    typed downstream[] fan-out. Allowed: absent, or {note: "..."} rationale.
VISIBILITY="$(jq -r '.visibility' "${METADATA}")"
DOWNSTREAM_TYPE="$(jq -r '.dependencies.downstream | if type == "array" then "array" elif type == "object" then (if has("note") and (.note | type == "string") then "note" else "object" end) else type end' "${METADATA}" 2>/dev/null || echo "null")"
if [[ "${VISIBILITY}" == "public" && "${DOWNSTREAM_TYPE}" == "array" ]]; then
  fail_msg "public repo must not carry typed dependencies.downstream[] (private-repo identifiers leak; use an anonymous {note} rationale) - see #168"
fi
if [[ "${DOWNSTREAM_TYPE}" == "object" ]]; then
  fail_msg "dependencies.downstream object is missing its anonymous rationale note"
fi

if [[ "${fail}" -eq 0 ]]; then
  echo "[INFO] metadata-schema: specs/metadata.json structurally valid"
  exit 0
fi
exit 1
