"""Contract tests: the ui-verify preset carries PR #193's template delta exactly.

Parity oracles are frozen fixture files - no VCS access, so the suite stays
green on shallow CI checkouts and on Windows (explicit UTF-8 decoding; the
tasks template contains non-ASCII emoji that a locale-decoded ``git show``
would mangle on cp1252):

- fixtures/ui_verify/parent/: fork templates BEFORE PR #193 (== upstream
  v1.4.0 core), extracted from git ``503028c2`` on 2026-11-12
- fixtures/ui_verify/with_pr193/: fork templates with PR #193 applied,
  extracted from git ``5cc91cf0`` on 2026-11-12

The preset contributions must byte-equal the with_pr193 fixtures, and every
changed region vs the parent must be conditional UI-VERIFY content (or the
checklist CHK renumbering the insertion forces).

Generated-output non-UI identity is already proven by
tests/test_ui_verify_template_contract.py (six contract tests); these tests
pin the preset packaging layer on top of that evidence instead of re-proving
it.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path

import pytest

from specify_cli.presets import PresetManifest

REPO_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = REPO_ROOT / "presets" / "ui-verify"
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "ui_verify"
TEMPLATE_NAMES = ["spec-template.md", "tasks-template.md", "checklist-template.md"]

# One distinctive marker per PR #193 addition, per template. Each must be
# present in the contribution and absent from the parent: the extraction may
# not smuggle in anything beyond the recorded delta.
DELTA_MARKERS = {
    "spec-template.md": [
        "**UI Surface** *(include if any user story has a rendered interface)*",
        'UI-surface stories only: make at least one "Then"',
    ],
    "tasks-template.md": [
        "### UI Verification for User Story 1 (ONLY if spec.md declares UI Surface)",
        "a failed UI-VERIFY blocks the story Checkpoint",
        "**Findings contract**: report each finding as step / expected / actual",
    ],
    "checklist-template.md": [
        "## UI Requirements Quality *(include if the spec declares UI Surface)*",
        "CHK004 Every UI-facing acceptance scenario names concrete visible expectations",
    ],
}

# Phrases that mark a delta region as conditional (generation-time omittable
# for non-UI features). The tasks/checklist sections gate via ONLY-if/include-if
# wording; the spec-template story comment gates via "UI-surface stories only".
_CONDITIONAL_ANCHORS = ("include if", "ONLY if", "UI-surface stories only")

# Checklist insertion forces CHK004-006 -> CHK007-009 renumbering in the next
# category; those replaced lines are delta content without a conditional marker.
_RENUMBER_RE = re.compile(r"^- \[ \] CHK\d{3} ")


def _fixture(kind: str, name: str) -> str:
    return (FIXTURES / kind / name).read_text(encoding="utf-8")


def _contribution(name: str) -> str:
    return (PRESET_DIR / "templates" / name).read_text(encoding="utf-8")


def test_manifest_validates_with_replace_contributions():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    assert manifest.data["preset"]["id"] == "ui-verify"
    templates = manifest.data["provides"]["templates"]
    by_name = {t["name"]: t for t in templates}
    assert sorted(by_name) == [
        "checklist-template",
        "spec-template",
        "tasks-template",
    ]
    assert all(t["type"] == "template" for t in templates)
    assert all(t.get("strategy", "replace") == "replace" for t in templates)
    assert manifest.data["requires"]["speckit_version"]


def test_declared_template_files_exist():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")
    for tmpl in manifest.data["provides"]["templates"]:
        assert (PRESET_DIR / tmpl["file"]).is_file(), tmpl["file"]


@pytest.mark.parametrize("name", TEMPLATE_NAMES)
def test_contribution_byte_equals_fork_template_with_pr193(name):
    assert _contribution(name) == _fixture("with_pr193", name)


@pytest.mark.parametrize("name", TEMPLATE_NAMES)
def test_contribution_contains_pr193_markers_absent_from_parent(name):
    parent = _fixture("parent", name)
    contribution = _contribution(name)
    assert contribution != parent, f"{name} carries no delta"
    for marker in DELTA_MARKERS[name]:
        assert marker in contribution, f"delta marker missing from {name}: {marker}"
        assert marker not in parent, (
            f"marker not introduced by PR #193 in {name}: {marker}"
        )


@pytest.mark.parametrize("name", TEMPLATE_NAMES)
def test_delta_regions_are_conditional_or_renumbering(name):
    """Every changed region vs the parent is conditional UI content.

    Inserted/replaced line blocks must either carry a conditional anchor
    (generation omits them for non-UI features) or consist solely of CHK
    renumbering lines. This is the template-level counterpart of the
    generated-output byte-identity proven in
    tests/test_ui_verify_template_contract.py.
    """
    parent_lines = _fixture("parent", name).splitlines(keepends=True)
    contribution_lines = _contribution(name).splitlines(keepends=True)
    matcher = difflib.SequenceMatcher(a=parent_lines, b=contribution_lines)
    blocks: list[list[str]] = []
    current: list[str] = []
    for op, _i1, _i2, j1, j2 in matcher.get_opcodes():
        if op in {"insert", "replace"}:
            current.extend(contribution_lines[j1:j2])
        elif current:
            blocks.append(current)
            current = []
    if current:
        blocks.append(current)

    assert blocks, f"{name} has no changed regions vs parent"
    for block in blocks:
        text = "".join(block)
        has_anchor = any(anchor in text for anchor in _CONDITIONAL_ANCHORS)
        renumber_only = all(_RENUMBER_RE.match(line) for line in block)
        assert has_anchor or renumber_only, (
            f"{name}: non-conditional delta region: {text!r}"
        )
