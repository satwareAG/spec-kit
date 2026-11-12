"""Contract tests: the ui-verify preset carries PR #193's template delta exactly.

Parity oracles are frozen git objects:
- parent ``503028c2``: fork templates BEFORE PR #193 (== upstream v1.4.0 core)
- delta  ``5cc91cf0``: fork templates with PR #193 applied

The preset contributions must byte-equal the delta templates and differ from
the parent only by the conditional UI-VERIFY additions. Generated-output
non-UI identity is already proven by tests/test_ui_verify_template_contract.py
(six contract tests); these tests pin the preset packaging layer on top of
that evidence instead of re-proving it.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from specify_cli.presets import PresetManifest

REPO_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = REPO_ROOT / "presets" / "ui-verify"
DELTA_SHA = "5cc91cf0"
PARENT_SHA = "503028c2"
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


def _git_show(rev: str, name: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{rev}:templates/{name}"],
        capture_output=True,
        text=True,
        check=True,
        cwd=REPO_ROOT,
    )
    return result.stdout


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
    assert _contribution(name) == _git_show(DELTA_SHA, name)


@pytest.mark.parametrize("name", TEMPLATE_NAMES)
def test_contribution_differs_from_parent_only_by_conditional_delta(name):
    parent = _git_show(PARENT_SHA, name)
    contribution = _contribution(name)
    assert contribution != parent, f"{name} carries no delta"
    for marker in DELTA_MARKERS[name]:
        assert marker in contribution, f"delta marker missing from {name}: {marker}"
        assert marker not in parent, (
            f"marker not introduced by PR #193 in {name}: {marker}"
        )
