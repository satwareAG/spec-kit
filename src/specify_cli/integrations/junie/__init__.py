"""Integration for Junie."""

from __future__ import annotations

from ..base import MarkdownIntegration


class JunieIntegration(MarkdownIntegration):
    """Integration for Junie."""

    key = "junie"
    config = {
        "name": "Junie",
        "folder": ".junie/",
        "commands_subdir": "commands",
        "install_url": "https://github.com/JetBrains/junie",
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".junie/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".junie/rules"
