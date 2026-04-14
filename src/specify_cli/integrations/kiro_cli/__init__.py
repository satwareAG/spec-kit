"""Integration for Kiro CLI."""

from __future__ import annotations

from ..base import MarkdownIntegration


class KiroCliIntegration(MarkdownIntegration):
    """Integration for Kiro CLI."""

    key = "kiro-cli"
    config = {
        "name": "Kiro CLI",
        "folder": ".kiro/",
        "commands_subdir": "prompts",
        "install_url": "https://kiro.dev/docs/cli/",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".kiro/prompts",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".kiro/rules"
