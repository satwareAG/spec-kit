"""Contract tests for the Abuse & Misuse Cases spec-template section (#151).

The section is the fork-side guarantee that authorization-abuse, injection,
and resource-abuse scenarios are written into every spec: no downstream
review or CI gate can infer an unwritten requirement. These tests exist so
upstream syncs cannot silently drop the section (same regression-contract
role as ``test_fork_agent_parity.py``).
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC_TEMPLATE = REPO_ROOT / "templates" / "spec-template.md"
CLARIFY_COMMAND = REPO_ROOT / "templates" / "commands" / "clarify.md"

REQUIRED_CATEGORIES = (
    "Unauthorized access",
    "Input & injection",
    "Rate & resource abuse",
)


def _extract_section(text: str, start: str, stop: str) -> str:
    start_idx = text.index(start)
    stop_idx = text.index(stop, start_idx)
    return text[start_idx:stop_idx]


def test_spec_template_has_abuse_misuse_section() -> None:
    """Negative control: fails on templates without the section (pre-#151)."""
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    assert "## Abuse & Misuse Cases" in text


def test_abuse_section_position_between_edge_cases_and_requirements() -> None:
    """Section lands after Edge Cases and before the Requirements heading."""
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    edge_idx = text.index("### Edge Cases")
    abuse_idx = text.index("## Abuse & Misuse Cases")
    req_idx = text.index("## Requirements")
    assert edge_idx < abuse_idx < req_idx


def test_abuse_section_lists_all_required_categories() -> None:
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    section = _extract_section(text, "## Abuse & Misuse Cases", "## Requirements")
    for category in REQUIRED_CATEGORIES:
        assert category in section, f"missing required category: {category}"


def test_abuse_section_mandates_negative_scenarios_and_fr_mapping() -> None:
    """Every case must be a Given/When/Then negative scenario mapped to an FR."""
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    section = _extract_section(text, "## Abuse & Misuse Cases", "## Requirements")
    assert "Given" in section and "When" in section and "Then" in section
    assert "FR-" in section


def test_abuse_section_references_owasp_a04() -> None:
    """The section must cross-reference OWASP Top 10 (2021) A04:2021 (Insecure Design)."""
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    section = _extract_section(text, "## Abuse & Misuse Cases", "## Requirements")
    assert "A04:2021" in section
    assert "Insecure Design" in section


def test_clarify_command_forces_security_abuse_question() -> None:
    """Clarify must force the abuse/misuse question when Security is Missing."""
    text = CLARIFY_COMMAND.read_text(encoding="utf-8")
    lowered = text.lower()
    assert "abuse" in lowered and "misuse" in lowered
    assert "question #1" in lowered or "first question" in lowered
