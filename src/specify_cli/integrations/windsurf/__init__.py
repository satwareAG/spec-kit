"""Integration for Windsurf."""

from __future__ import annotations

from ..base import MarkdownIntegration


class WindsurfIntegration(MarkdownIntegration):
    """Integration for Windsurf."""

    key = "windsurf"
    config = {
        "name": "Windsurf",
        "folder": ".windsurf/",
        "commands_subdir": "workflows",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".windsurf/workflows",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".windsurf/rules"
