"""Integration for Generic (bring your own agent)."""

from __future__ import annotations

from ..base import MarkdownIntegration


class GenericIntegration(MarkdownIntegration):
    """Integration for Generic (bring your own agent)."""

    key = "generic"
    config = {
        "name": "Generic (bring your own agent)",
        "folder": None,
        "commands_subdir": "commands",
        "install_url": None,
        "requires_cli": False,
    }
    registrar_config = None
    context_file = None
