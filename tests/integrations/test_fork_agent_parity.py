"""IPADP Phase 4.3 (issue #24) — Fork-agent parity audit.

Originally asserted structural parity for agents the fork added ahead of
upstream (``agy``, ``bob``, ``iflow``, ``kimi``, ``hermes``, ``cline``).
All six have since been accepted into upstream github/spec-kit (by v0.11.8),
so this module now serves as regression coverage: it verifies the agents the
fork originated still register, satisfy the ``IntegrationBase`` structural
contract, and run end-to-end via ``specify init``.

Structural contract checks:

- declares ``key``, ``config``, ``registrar_config``, ``context_file``
- ``context_file`` is a non-empty string
- registers in the global registry
- ``specify init --integration <key>`` succeeds and produces the configured
  commands directory.
"""
from __future__ import annotations

import os

import pytest

from specify_cli.integrations import get_integration
from specify_cli.integrations.base import IntegrationBase


# Agents originated by this fork; all have since been upstreamed.
# Kept as regression coverage for the fork's contribution.
FORK_AGENTS = ["agy", "bob", "iflow", "kimi", "hermes", "cline"]

REQUIRED_CONFIG_KEYS = {"name", "folder", "commands_subdir", "install_url", "requires_cli"}
REQUIRED_REGISTRAR_KEYS = {"dir", "format", "args", "extension"}


@pytest.mark.parametrize("key", FORK_AGENTS)
class TestForkAgentParity:
    """Structural parity checks for each fork-only integration."""

    def test_registered(self, key):
        integration = get_integration(key)
        assert integration is not None, f"Fork agent {key!r} not registered"
        assert isinstance(integration, IntegrationBase)

    def test_key_matches(self, key):
        assert get_integration(key).key == key

    def test_config_shape(self, key):
        config = get_integration(key).config
        assert isinstance(config, dict)
        missing = REQUIRED_CONFIG_KEYS - set(config)
        assert not missing, f"{key}: config missing keys {missing}"
        assert isinstance(config["requires_cli"], bool)
        assert isinstance(config["name"], str) and config["name"]
        assert isinstance(config["folder"], str) and config["folder"]

    def test_registrar_config_shape(self, key):
        rc = get_integration(key).registrar_config
        assert isinstance(rc, dict)
        missing = REQUIRED_REGISTRAR_KEYS - set(rc)
        assert not missing, f"{key}: registrar_config missing keys {missing}"
        assert rc["format"] in {"markdown", "toml", "yaml"}

    def test_context_file_nonempty(self, key):
        cf = get_integration(key).context_file
        assert isinstance(cf, str) and cf.strip(), (
            f"{key}: context_file must be a non-empty string"
        )

    def test_specify_init_succeeds(self, key, tmp_path):
        """End-to-end: `specify init --integration <key>` must produce
        the configured commands directory without errors."""
        if key == "hermes":
            pytest.skip(
                "Hermes installs to the user-global ~/.hermes/skills, not a "
                "project-local dir; covered by test_integration_hermes.py"
            )
        from typer.testing import CliRunner
        from specify_cli import app

        integration = get_integration(key)
        project = tmp_path / f"parity-{key}"
        project.mkdir()
        old_cwd = os.getcwd()
        try:
            os.chdir(project)
            result = CliRunner().invoke(app, [
                "init", "--here", "--integration", key,
                "--script", "sh", "--ignore-agent-tools",
            ], catch_exceptions=False)
        finally:
            os.chdir(old_cwd)

        assert result.exit_code == 0, f"init failed for {key}: {result.output}"

        commands_dir = project / integration.registrar_config["dir"]
        assert commands_dir.exists(), (
            f"{key}: expected commands dir {commands_dir} not created"
        )
        # Commands dir should contain at least one generated file.
        produced = list(commands_dir.rglob("*"))
        produced_files = [p for p in produced if p.is_file()]
        assert produced_files, f"{key}: no command files produced in {commands_dir}"
