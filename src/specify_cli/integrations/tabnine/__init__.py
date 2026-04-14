"""Integration for Tabnine CLI."""

from __future__ import annotations

from ..base import TomlIntegration


class TabnineIntegration(TomlIntegration):
    """Integration for Tabnine CLI."""

    key = "tabnine"
    config = {
        "name": "Tabnine CLI",
        "folder": ".tabnine/agent/",
        "commands_subdir": "commands",
        "install_url": "https://docs.tabnine.com/main/getting-started/tabnine-cli",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".tabnine/agent/commands",
        "format": "toml",
        "args": "{{args}}",
        "extension": ".toml",
    }
    context_file = ".tabnine/rules"
