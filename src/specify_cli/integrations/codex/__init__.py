"""Integration for Codex CLI."""

from __future__ import annotations

from ..base import SkillsIntegration


class CodexIntegration(SkillsIntegration):
    """Integration for Codex CLI."""

    key = "codex"
    config = {
        "name": "Codex CLI",
        "folder": ".codex/",
        "commands_subdir": "prompts",
        "install_url": "https://github.com/openai/codex",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".codex/prompts",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": "/SKILL.md",
    }
    context_file = "codex.md"
