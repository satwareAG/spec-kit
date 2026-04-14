"""Integration for GitHub Copilot."""

from __future__ import annotations

from ..base import MarkdownIntegration


class CopilotIntegration(MarkdownIntegration):
    """Integration for GitHub Copilot."""

    key = "copilot"
    config = {
        "name": "GitHub Copilot",
        "folder": ".github/",
        "commands_subdir": "agents",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".github/agents",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = "copilot-instructions.md"
