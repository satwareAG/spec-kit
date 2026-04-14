"""Integration for Cline CLI."""

from __future__ import annotations

from ..base import MarkdownIntegration


class ClineIntegration(MarkdownIntegration):
    """Integration for Cline CLI."""

    key = "cline"
    config = {
        "name": "Cline CLI",
        "folder": ".cline/",
        "commands_subdir": "commands",
        "install_url": "https://github.com/cline/cline",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".cline/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".cline/rules"
