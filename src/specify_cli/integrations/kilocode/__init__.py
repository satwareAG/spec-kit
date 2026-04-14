"""Integration for Kilo Code."""

from __future__ import annotations

from ..base import MarkdownIntegration


class KilocodeIntegration(MarkdownIntegration):
    """Integration for Kilo Code."""

    key = "kilocode"
    config = {
        "name": "Kilo Code",
        "folder": ".kilocode/",
        "commands_subdir": "workflows",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = {
        "dir": ".kilocode/workflows",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".kilocode/rules"
