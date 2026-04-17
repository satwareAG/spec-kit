# Feature Specification: Upstream Release Sync Strategy

**Feature Branch**: `spec/upstream-release-sync-strategy`
**Created**: 2026-04-17
**Status**: Draft
**Input**: Keep satwareAG/spec-kit fork updated with upstream release versions only, while preserving custom agent integrations (cline, hermes) as part of IPADP.

## Context

This fork (`satwareAG/spec-kit`) adds proprietary agent integrations (cline, hermes) on top of the upstream `github/spec-kit` project. As IPADP project #6, it must maintain conformance with released upstream versions while carrying custom additions.

### Current State

| Item | Value |
|------|-------|
| Fork version | 0.7.2 (matches upstream release tag `v0.7.2`) |
| Upstream main | 0.7.3.dev0 (unreleased development) |
| Custom files | 10 files: cline integration, hermes integration, shared scripts |
| Upstream drift | 3 commits ahead of `v0.7.2` tag (all dev-phase, no release) |

### Custom Fork Additions (must survive sync)

| File | Purpose |
|------|---------|
| `src/specify_cli/integrations/cline/` | Cline agent integration |
| `src/specify_cli/integrations/hermes/` | Hermes agent integration |
| `src/specify_cli/integrations/__init__.py` | Modified to register cline/hermes |
| `scripts/bash/update-agent-context.sh` | Modified to include cline/hermes |
| `scripts/powershell/update-agent-context.ps1` | Modified to include cline/hermes |
| `CHANGELOG.md` | Fork-specific changelog |
| `pyproject.toml` | Version bumped with fork additions |

## User Scenarios & Testing

### User Story 1 - Sync to New Upstream Release (Priority: P1)

As a maintainer, when upstream publishes a new release tag (e.g., `v0.7.3`), I can merge it into the fork while preserving all custom integrations, and the full test suite passes.

**Why this priority**: Core workflow - without clean sync, fork drifts and becomes unmaintainable.

**Independent Test**: Checkout fork, merge upstream tag `v0.7.3`, run test suite, verify cline/hermes integrations still registered and functional.

### User Story 2 - Skip Unreleased Development Commits (Priority: P1)

As a maintainer, I can distinguish between released and unreleased upstream commits and only merge released versions, preventing dev-phase instability from affecting the fork.

**Why this priority**: Stability guarantee - upstream `main` contains unreleased changes (e.g., `0.7.3.dev0`) that must not be merged prematurely.

**Independent Test**: `git log upstream/main..v0.7.2` shows only unreleased commits; fork ignores them until tag appears.

### User Story 3 - Resolve Merge Conflicts in Shared Files (Priority: P2)

As a maintainer, when upstream modifies shared files (e.g., `integrations/__init__.py`, `update-agent-context.sh`) that also have custom additions, I can resolve conflicts with a documented procedure that preserves both upstream and custom changes.

**Why this priority**: Conflict resolution is the highest-risk operation; documented procedure prevents accidental loss.

**Independent Test**: Simulate conflict by cherry-picking an upstream commit touching `__init__.py`, resolve using procedure, verify both upstream and custom integrations registered.

### User Story 4 - Validate Fork Integrity After Sync (Priority: P2)

As a maintainer, after syncing to a new release, I can run a validation procedure that confirms fork integrity: correct version, all integrations registered, all tests passing.

**Why this priority**: Quality gate - catches sync issues before push.

**Independent Test**: Run validation script, confirm all checks pass (version matches tag, `specify --help` lists cline/hermes, tests green).

### User Story 5 - Automated Sync Detection (Priority: P3)

As a maintainer, I receive awareness (via morning protocol or CI) when a new upstream release tag is available for merging.

**Why this priority**: Convenience - prevents missed releases without manual checking.

**Independent Test**: Morning health check or CI job reports "upstream release v0.7.3 available" when tag exists but is not merged.

## Requirements

### FR-001: Release-Only Merge Policy

The fork MUST only merge upstream changes at tagged release commits (e.g., `v0.7.3`), NOT from `upstream/main` HEAD which may contain unreleased development code.

**Constraint**: Upstream uses `X.Y.Z` semver tags. Dev versions appear as `X.Y.(Z+1).dev0` commits on main between tags.

### FR-002: Custom Integration Preservation

All custom files (cline, hermes integrations and shared script modifications) MUST survive upstream merges without functional regression.

### FR-003: Version Alignment

After sync, `pyproject.toml` version MUST match the merged upstream release tag.

### FR-004: Test Suite Validation

After sync, the full test suite (`pytest tests/`) MUST pass with 0 failures.

### FR-005: Conflict Resolution Procedure

A documented procedure MUST exist for resolving conflicts in shared files (`integrations/__init__.py`, `update-agent-context.sh/ps1`) that preserves both upstream additions and custom registrations.

### FR-006: IPADP Conformance

The fork MUST maintain `AGENTS.md`, `specs/metadata.json` with upstream/downstream relationships, and privacy validation per IPADP L1-L3 conformance requirements.

## Constraints

- **No upstream PRs**: This is a fork with additions; we do not contribute custom integrations upstream.
- **No dev-version merges**: `upstream/main` HEAD is NOT a valid merge target; only tagged releases.
- **Semantic versioning**: Fork version equals upstream version (no fork-specific version suffix).

## Success Criteria

| Criteria | Measurement |
|----------|-------------|
| Sync completes cleanly | Merge of upstream tag produces no unresolved conflicts or at most documented resolution steps |
| All tests pass | `pytest tests/` returns 0 failures |
| Integrations functional | `specify init --help` lists cline and hermes as available integrations |
| Version correct | `pyproject.toml` version matches merged tag |
| No custom code lost | `git diff` shows cline/hermes files intact post-merge |

## Sync Procedure (Reference Implementation)

```bash
# 1. Fetch upstream tags
git fetch upstream --tags

# 2. Check latest release tag
LATEST_TAG=$(git tag -l 'v*' --sort=-v:refname | head -1)

# 3. Verify not already merged
git merge-base --is-ancestor $LATEST_TAG HEAD && echo "Already merged" && exit 0

# 4. Merge tag (not main)
git merge $LATEST_TAG --no-edit

# 5. Resolve conflicts in shared files if any
#    - integrations/__init__.py: keep both upstream registrations AND custom cline/hermes
#    - update-agent-context.sh/ps1: keep both upstream agents AND cline/hermes cases

# 6. Update version in pyproject.toml to match tag

# 7. Validate
uv run pytest tests/ -x -q

# 8. Commit and push
git push origin HEAD
```

## Out of Scope

- Automated CI sync (future consideration)
- Upstream contribution of custom integrations
- Fork-specific versioning scheme