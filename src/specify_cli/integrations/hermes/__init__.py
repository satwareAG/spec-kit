"""Integration for Hermes CLI."""

from __future__ import annotations

from ..base import MarkdownIntegration


class HermesIntegration(MarkdownIntegration):
    """Integration for Hermes CLI."""

    key = "hermes"
    config = {
        "name": "Hermes CLI",
        "folder": ".hermes/",
        "commands_subdir": "skills",
        "install_url": "https://github.com/nousresearch/hermes",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".hermes/skills",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = "SOUL.md"