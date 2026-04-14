"""Integration for IBM Bob."""

from __future__ import annotations

from ..base import MarkdownIntegration


class BobIntegration(MarkdownIntegration):
    """Integration for IBM Bob."""

    key = "bob"
    config = {
        "name": "IBM Bob",
        "folder": ".bob/",
        "commands_subdir": "commands",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".bob/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".bob/rules"
