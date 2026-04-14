"""Integration for Hermes."""

from __future__ import annotations

from ..base import MarkdownIntegration


class HermesIntegration(MarkdownIntegration):
    """Integration for Hermes."""

    key = "hermes"
    config = {
        "name": "Hermes",
        "folder": ".hermes/",
        "commands_subdir": "commands",
        "install_url": "https://github.com/NousResearch/hermes-agent",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".hermes/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = "SOUL.md"
