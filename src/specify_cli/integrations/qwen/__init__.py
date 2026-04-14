"""Integration for Qwen Code."""

from __future__ import annotations

from ..base import TomlIntegration


class QwenIntegration(TomlIntegration):
    """Integration for Qwen Code."""

    key = "qwen"
    config = {
        "name": "Qwen Code",
        "folder": ".qwen/",
        "commands_subdir": "commands",
        "install_url": "https://github.com/QwenLM/qwen-code",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".qwen/commands",
        "format": "toml",
        "args": "{{args}}",
        "extension": ".toml",
    }
    context_file = ".qwen/rules"
