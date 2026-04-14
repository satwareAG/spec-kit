"""Integration for Roo Code."""

from __future__ import annotations

from ..base import MarkdownIntegration


class RooIntegration(MarkdownIntegration):
    """Integration for Roo Code."""

    key = "roo"
    config = {
        "name": "Roo Code",
        "folder": ".roo/",
        "commands_subdir": "commands",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".roo/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".roo/rules"
