"""Integration for Antigravity."""

from __future__ import annotations

from ..base import MarkdownIntegration


class AgyIntegration(MarkdownIntegration):
    """Integration for Antigravity."""

    key = "agy"
    config = {
        "name": "Antigravity",
        "folder": ".agent/",
        "commands_subdir": "workflows",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".agent/workflows",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".agent/rules"
