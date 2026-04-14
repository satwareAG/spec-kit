"""Integration for CodeBuddy."""

from __future__ import annotations

from ..base import MarkdownIntegration


class CodebuddyIntegration(MarkdownIntegration):
    """Integration for CodeBuddy."""

    key = "codebuddy"
    config = {
        "name": "CodeBuddy",
        "folder": ".codebuddy/",
        "commands_subdir": "commands",
        "install_url": "https://www.codebuddy.ai/cli",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".codebuddy/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".codebuddy/rules"
