"""Integration for Claude Code."""

from __future__ import annotations

from ..base import SkillsIntegration


class ClaudeIntegration(SkillsIntegration):
    """Integration for Claude Code."""

    key = "claude"
    config = {
        "name": "Claude Code",
        "folder": ".claude/",
        "commands_subdir": "skills",
        "install_url": "https://docs.anthropic.com/en/docs/claude-code/setup",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".claude/skills",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": "/SKILL.md",
    }
    context_file = "CLAUDE.md"
