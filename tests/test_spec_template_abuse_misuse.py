"""The spec template must mandate Abuse & Misuse Cases (#151).

Misuse cases (IDOR/BOLA, injection, resource abuse) are otherwise captured
only probabilistically: the clarify security category competes for a max-5
question budget, and Edge Cases never mandates authorization abuse. No
downstream gate can infer an unwritten requirement, so a missing "deny
cross-user access" rule ships as green code.
"""

from pathlib import Path

SPEC_TEMPLATE = Path(__file__).parent.parent / "templates" / "spec-template.md"
CLARIFY = Path(__file__).parent.parent / "templates" / "commands" / "clarify.md"

SECTION_HEADING = "## Abuse & Misuse Cases"
REQUIRED_CATEGORIES = (
    "Unauthorized access",
    "Input & injection",
    "Rate & resource abuse",
)


def _abuse_section(text: str) -> str:
    start = text.index(SECTION_HEADING)
    end = text.index("## Requirements")
    return text[start:end]


def test_spec_template_has_abuse_misuse_section_between_edge_cases_and_requirements() -> None:
    text = SPEC_TEMPLATE.read_text(encoding="utf-8")
    assert SECTION_HEADING in text
    assert text.index("### Edge Cases") < text.index(SECTION_HEADING)
    assert text.index(SECTION_HEADING) < text.index("## Requirements")


def test_abuse_misuse_section_names_required_categories() -> None:
    section = _abuse_section(SPEC_TEMPLATE.read_text(encoding="utf-8"))
    for category in REQUIRED_CATEGORIES:
        assert category in section, f"missing required category: {category}"


def test_abuse_misuse_section_maps_cases_to_requirements() -> None:
    section = _abuse_section(SPEC_TEMPLATE.read_text(encoding="utf-8"))
    # Negative scenarios in Given/When/Then form, each mapped to an FR.
    assert "**Given**" in section
    assert "**When**" in section
    assert "**Then**" in section
    assert "FR-" in section


def test_clarify_forces_abuse_misuse_question_on_security_gap() -> None:
    text = CLARIFY.read_text(encoding="utf-8")
    assert "Abuse & Misuse Cases" in text
    assert "first clarification question" in text
