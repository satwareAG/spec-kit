"""Integration for Mistral Vibe."""

from __future__ import annotations

from ..base import MarkdownIntegration


class VibeIntegration(MarkdownIntegration):
    """Integration for Mistral Vibe."""

    key = "vibe"
    config = {
        "name": "Mistral Vibe",
        "folder": ".vibe/",
        "commands_subdir": "prompts",
        "install_url": "https://github.com/mistralai/mistral-vibe",
        "requires_cli": True,
    }
    registrar_config = {
        "dir": ".vibe/prompts",
        "format": "markdown",
        "args": "$ARGUMENTS",
        "extension": ".md",
    }
    context_file = ".vibe/rules"
