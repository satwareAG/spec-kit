"""Integration for Qoder CLI."""

from __future__ import annotations

from ..base import MarkdownIntegration


class QodercliIntegration(MarkdownIntegration):
    """Integration for Qoder CLI."""

    key = "qodercli"
    config = {
        "name": "Qoder CLI",
        "folder": ".qoder/",
        "commands_subdir": "commands",
        "install_url": "https://qoder.com/cli",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".qoder/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".qoder/rules"
