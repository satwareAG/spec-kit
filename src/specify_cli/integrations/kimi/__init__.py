"""Integration for Kimi Code."""

from __future__ import annotations

from ..base import SkillsIntegration


class KimiIntegration(SkillsIntegration):
    """Integration for Kimi Code."""

    key = "kimi"
    config = {
        "name": "Kimi Code",
        "folder": ".kimi/",
        "commands_subdir": "skills",
        "install_url": "https://code.kimi.com/",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".kimi/skills",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": "/SKILL.md",
    }
    context_file = ".kimi/rules"
