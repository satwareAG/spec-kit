"""Integration for Auggie CLI."""

from __future__ import annotations

from ..base import MarkdownIntegration


class AuggieIntegration(MarkdownIntegration):
    """Integration for Auggie CLI."""

    key = "auggie"
    config = {
        "name": "Auggie CLI",
        "folder": ".augment/",
        "commands_subdir": "commands",
        "install_url": "https://docs.augmentcode.com/cli/setup-auggie/install-auggie-cli",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".augment/commands",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".augment/rules"
