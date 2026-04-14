"""Tests for P1 addon command templates (orchestrate + env-schema).

Validates that the new command templates exist, have correct frontmatter,
are included in SKILL_DESCRIPTIONS, and follow established patterns.
"""

import pytest
from pathlib import Path
import yaml

# Project root
ROOT = Path(__file__).parent.parent
TEMPLATES_DIR = ROOT / "templates" / "commands"
INIT_FILE = ROOT / "src" / "specify_cli" / "__init__.py"


class TestOrchestrateTemplate:
    """Tests for the /speckit.orchestrate command template."""

    TEMPLATE = TEMPLATES_DIR / "orchestrate.md"

    def test_template_exists(self):
        assert self.TEMPLATE.exists(), "orchestrate.md template must exist"

    def test_has_frontmatter(self):
        content = self.TEMPLATE.read_text()
        assert content.startswith("---"), "Must start with YAML frontmatter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, "Must have opening and closing ---"

    def test_frontmatter_has_description(self):
        content = self.TEMPLATE.read_text()
        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert "description" in fm, "Must have description in frontmatter"
        assert len(fm["description"]) > 20, "Description should be meaningful"

    def test_frontmatter_has_handoffs(self):
        content = self.TEMPLATE.read_text()
        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert "handoffs" in fm, "Should define handoffs to related commands"

    def test_mentions_taskfile(self):
        content = self.TEMPLATE.read_text().lower()
        assert "taskfile" in content, "Must mention Taskfile format"

    def test_mentions_makefile(self):
        content = self.TEMPLATE.read_text().lower()
        assert "makefile" in content, "Must mention Makefile fallback"

    def test_mentions_standard_targets(self):
        content = self.TEMPLATE.read_text()
        for target in ["generate", "validate", "smoke-test", "deploy"]:
            assert target in content, f"Must mention '{target}' target"

    def test_has_quality_checks(self):
        content = self.TEMPLATE.read_text()
        assert "Quality Checks" in content or "quality checks" in content.lower(), \
            "Must have quality checks section"


class TestEnvSchemaTemplate:
    """Tests for the /speckit.env-schema command template."""

    TEMPLATE = TEMPLATES_DIR / "env-schema.md"

    def test_template_exists(self):
        assert self.TEMPLATE.exists(), "env-schema.md template must exist"

    def test_has_frontmatter(self):
        content = self.TEMPLATE.read_text()
        assert content.startswith("---"), "Must start with YAML frontmatter"
        parts = content.split("---", 2)
        assert len(parts) >= 3, "Must have opening and closing ---"

    def test_frontmatter_has_description(self):
        content = self.TEMPLATE.read_text()
        parts = content.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert "description" in fm, "Must have description in frontmatter"
        assert len(fm["description"]) > 20

    def test_mentions_env_schema(self):
        content = self.TEMPLATE.read_text()
        assert ".env.schema" in content, "Must mention .env.schema file"

    def test_mentions_secret_handling(self):
        content = self.TEMPLATE.read_text().lower()
        assert "secret" in content, "Must cover secret handling"

    def test_mentions_ref_pattern(self):
        content = self.TEMPLATE.read_text()
        assert "_ref" in content, "Must mention _ref pattern for secrets"

    def test_mentions_env_example(self):
        content = self.TEMPLATE.read_text()
        assert ".env.example" in content, "Must mention .env.example generation"

    def test_mentions_variable_types(self):
        content = self.TEMPLATE.read_text()
        for vtype in ["string", "integer", "boolean", "enum"]:
            assert vtype in content, f"Must mention '{vtype}' type"

    def test_has_quality_checks(self):
        content = self.TEMPLATE.read_text()
        assert "Quality Checks" in content or "quality checks" in content.lower()


class TestSkillDescriptions:
    """Tests that new addons are in SKILL_DESCRIPTIONS."""

    @classmethod
    def _get_descriptions(cls):
        # Parse SKILL_DESCRIPTIONS from __init__.py
        content = INIT_FILE.read_text()
        # Just verify the keys exist by importing
        return True

    def test_orchestrate_in_descriptions(self):
        content = INIT_FILE.read_text()
        assert '"orchestrate"' in content, "orchestrate must be in SKILL_DESCRIPTIONS"

    def test_env_schema_in_descriptions(self):
        content = INIT_FILE.read_text()
        assert '"env-schema"' in content, "env-schema must be in SKILL_DESCRIPTIONS"

    def test_orchestrate_description_meaningful(self):
        content = INIT_FILE.read_text()
        # Find the orchestrate description line
        for line in content.splitlines():
            if '"orchestrate"' in line and "Taskfile" in line:
                assert "Makefile" in line, "Should mention both formats"
                assert "CI/CD" in line, "Should mention CI/CD"
                break
        else:
            pytest.fail("orchestrate description not found or incomplete")

    def test_env_schema_description_meaningful(self):
        content = INIT_FILE.read_text()
        for line in content.splitlines():
            if '"env-schema"' in line and ".env.schema" in line:
                assert "secret" in line.lower(), "Should mention secrets"
                break
        else:
            pytest.fail("env-schema description not found or incomplete")


class TestSpecFiles:
    """Tests that spec files exist for both addons."""

    def test_orchestrate_spec_exists(self):
        spec = ROOT / "specs" / "002-taskfile-generator" / "spec.md"
        assert spec.exists(), "Taskfile generator spec must exist"

    def test_env_schema_spec_exists(self):
        spec = ROOT / "specs" / "003-env-schema-validator" / "spec.md"
        assert spec.exists(), "Env schema validator spec must exist"

    def test_orchestrate_spec_has_requirements(self):
        content = (ROOT / "specs" / "002-taskfile-generator" / "spec.md").read_text()
        assert "FR-001" in content, "Must have functional requirements"

    def test_env_schema_spec_has_requirements(self):
        content = (ROOT / "specs" / "003-env-schema-validator" / "spec.md").read_text()
        assert "FR-001" in content, "Must have functional requirements"