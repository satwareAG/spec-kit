"""Integration tests: ui-verify preset install -> resolution -> uninstall.

Drives the real CLI (CliRunner) against a real project and a real
PresetManager/PresetResolver, following the
tests/integration/test_preset_update_workflow.py pattern.

Note on layers: ``.specify/templates/`` is the project-override layer and
BEATS presets, so the fixture project must not write templates there. Core
defaults resolve from the dev tree, and the preset must win the stack only
while it is installed; uninstall must restore the core resolution
byte-for-byte (frozen before-snapshot).
"""
from __future__ import annotations

from pathlib import Path

import pytest
from typer.testing import CliRunner

from specify_cli import app
from specify_cli.presets import PresetResolver

REPO_ROOT = Path(__file__).resolve().parents[2]
PRESET_DIR = REPO_ROOT / "presets" / "ui-verify"
PRESET_ID = "ui-verify"

RESOLUTION_MARKERS = {
    "spec-template": "**UI Surface**",
    "tasks-template": "ONLY if spec.md declares UI Surface",
    "checklist-template": "UI Requirements Quality",
}


@pytest.fixture
def project(tmp_path: Path, monkeypatch) -> Path:
    root = tmp_path / "proj"
    (root / ".specify").mkdir(parents=True)
    monkeypatch.chdir(root)
    return root


def _install(runner: CliRunner) -> None:
    result = runner.invoke(app, ["preset", "add", "--dev", str(PRESET_DIR)])
    assert result.exit_code == 0, result.output


def _top_source(project: Path, template_name: str) -> str:
    layers = PresetResolver(project).collect_all_layers(template_name, "template")
    assert layers, f"no resolution layers for {template_name}"
    return str(layers[0]["source"])


def _composed(project: Path, template_name: str) -> str:
    content = PresetResolver(project).resolve_content(template_name, "template")
    assert content is not None, f"no composed content for {template_name}"
    return content


def test_ui_verify_preset_installs_and_lists(project: Path):
    runner = CliRunner()
    _install(runner)

    installed_dir = project / ".specify" / "presets" / PRESET_ID
    assert (installed_dir / "preset.yml").is_file()

    listing = runner.invoke(app, ["preset", "list"])
    assert listing.exit_code == 0, listing.output
    assert PRESET_ID in listing.output


def test_resolution_uses_preset_layer_with_ui_verify_content(project: Path):
    runner = CliRunner()
    for template_name in RESOLUTION_MARKERS:
        assert "ui-verify" not in _top_source(project, template_name), (
            f"{template_name} must resolve to core before install"
        )

    _install(runner)

    for template_name, marker in RESOLUTION_MARKERS.items():
        assert "ui-verify" in _top_source(project, template_name), (
            f"preset layer must win resolution for {template_name}"
        )
        contribution = (PRESET_DIR / "templates" / f"{template_name}.md").read_text(
            encoding="utf-8"
        )
        assert _composed(project, template_name) == contribution, (
            f"replace strategy must compose to the contribution for {template_name}"
        )
        assert marker in _composed(project, template_name)


def test_uninstall_restores_core_resolution_byte_for_byte(project: Path):
    runner = CliRunner()
    before = {name: _composed(project, name) for name in RESOLUTION_MARKERS}

    _install(runner)
    removal = runner.invoke(app, ["preset", "remove", PRESET_ID])
    assert removal.exit_code == 0, removal.output

    installed_dir = project / ".specify" / "presets" / PRESET_ID
    assert not installed_dir.exists(), "uninstall must remove the preset files"

    after = {name: _composed(project, name) for name in RESOLUTION_MARKERS}
    assert after == before, "uninstall must restore core resolution byte-for-byte"
    for template_name in RESOLUTION_MARKERS:
        assert "ui-verify" not in _top_source(project, template_name)
