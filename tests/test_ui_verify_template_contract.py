"""Contract tests for the UI-VERIFY template additions (fork #190).

The spec/tasks/checklist templates gain conditional, tool-agnostic UI-surface
verification support: an explicit UI Surface declaration, browser-drive
acceptance guidance, a conditional UI Verification task section gated on the
spec declaration, and a requirement-quality checklist category. All additions
are strictly include-if so non-UI features generate unchanged output.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SPEC_TEMPLATE = REPO_ROOT / "templates" / "spec-template.md"
TASKS_TEMPLATE = REPO_ROOT / "templates" / "tasks-template.md"
CHECKLIST_TEMPLATE = REPO_ROOT / "templates" / "checklist-template.md"


def test_spec_template_declares_ui_surface_field():
    content = SPEC_TEMPLATE.read_text(encoding="utf-8")
    assert "**UI Surface** *(include if any user story has a rendered interface)*" in content, (
        "spec-template must carry an explicit include-if UI Surface declaration "
        "so UI-VERIFY tasks are generated only on explicit declaration"
    )
    assert "UI-VERIFY" in content or "UI Verification" in content, (
        "the UI Surface declaration must state what it drives"
    )


def test_spec_template_requires_concrete_rendered_expectations():
    content = SPEC_TEMPLATE.read_text(encoding="utf-8")
    assert "renders the acceptance output concretely" in content, (
        "spec-template must guide browser-drive scenarios toward concrete visible "
        "expectations (labels, header texts, formatted values)"
    )
    assert 'never "looks correct"' in content, (
        "the guidance must explicitly ban subjective 'looks correct' expectations"
    )


def test_tasks_template_has_conditional_ui_verification_section():
    content = TASKS_TEMPLATE.read_text(encoding="utf-8")
    assert "ONLY if" in content and "UI Surface" in content, (
        "tasks-template must gate the UI Verification section on the spec's "
        "UI Surface declaration"
    )
    assert "headless browser" in content, (
        "the UI-VERIFY task must drive scenarios in a headless browser"
    )
    assert "structural" in content.lower(), (
        "rendered-output assertions must prefer structural checks (DOM/text) "
        "over visual judgement"
    )
    assert "quickstart.md" in content, (
        "UI validation outcomes must fold into the existing quickstart.md "
        "validation convention (council D2)"
    )
    assert "blocks the story Checkpoint" in content, (
        "a failed UI-VERIFY must gate the story Checkpoint like the "
        "integration suite gates API stories"
    )


def test_tasks_template_carries_findings_contract():
    content = TASKS_TEMPLATE.read_text(encoding="utf-8")
    assert "Findings contract" in content
    assert "expected / actual" in content or "expected/actual" in content, (
        "findings must be reported as step / expected / actual"
    )
    assert "capture" in content.lower()
    assert "one root cause = one fix" in content
    assert "zero false positives" in content.lower(), (
        "every finding claim must carry its capture (zero false positives)"
    )


def test_checklist_template_ui_category_is_requirements_quality_only():
    content = CHECKLIST_TEMPLATE.read_text(encoding="utf-8")
    assert "UI Requirements Quality" in content, (
        "checklist gains a conditional UI Requirements Quality category "
        "(requirement quality only, per the checklist constitution)"
    )
    assert "include if" in content

    category = content.split("## UI Requirements Quality", 1)[1]
    banned_starts = ("verify", "test", "confirm", "check")
    for line in category.splitlines():
        stripped = line.lstrip("- [ ] ")
        if not stripped or stripped.startswith("["):
            continue
        first_word = stripped.split(" ", 1)[0].lower()
        assert first_word not in banned_starts, (
            f"checklist item must not be a verification item (got {stripped!r}); "
            "the checklist constitution bans Verify/Test/Confirm/Check items"
        )


def test_templates_stay_tool_agnostic():
    for template in (SPEC_TEMPLATE, TASKS_TEMPLATE, CHECKLIST_TEMPLATE):
        content = template.read_text(encoding="utf-8")
        assert "playwright" not in content.lower(), (
            f"{template.name} must not hardcode a browser tool brand; use "
            "'[e.g., any browser automation CLI ...]' example style"
        )
