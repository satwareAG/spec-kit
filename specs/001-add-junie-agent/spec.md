# Feature Specification: Add Junie Agent Support

**Feature Branch**: `001-add-junie-agent`
**Created**: 2026-03-12
**Status**: Draft

## User Scenarios & Testing

### User Story 1 - Use Junie as an AI Assistant (Priority: P1)

**Why this priority**: Junie is the current agent and should be natively supported to ensure consistent development patterns and easier initialization.

**Independent Test**:
1. Run `specify init . --ai junie` in a clean directory.
2. Verify that the `.junie/commands/` directory is created.
3. Verify that the standard SDD command templates are generated within `.junie/commands/`.

**Acceptance Scenarios**:
1. **Given** the Specify CLI is installed, **When** I run `specify init --ai junie`, **Then** the initialization completes successfully without requiring external CLI tool checks (since Junie is the current environment).
2. **Given** the project is initialized with Junie, **When** I check the `AGENT_CONFIG` in `src/specify_cli/__init__.py`, **Then** Junie should be listed with correct configuration.
3. **Given** the repository has an `AGENTS.md` file, **When** Junie support is added, **Then** `AGENTS.md` should be updated to include Junie in the supported agents table.

## Requirements

### Functional Requirements
- **FR-001**: Add `junie` to `AGENT_CONFIG` in `src/specify_cli/__init__.py`.
- **FR-002**: Configure Junie to use `.junie/` as the folder and `commands` as the `commands_subdir`.
- **FR-003**: Set `requires_cli` to `False` for Junie (as it's the environment itself).
- **FR-004**: Update the `--ai` option help text in `specify_cli` to include `junie`.
- **FR-005**: Update `README.md` to include Junie in the Supported AI Agents table.
- **FR-006**: Update `AGENTS.md` to include Junie in the current supported agents list and Step-by-Step Integration Guide examples if applicable.
- **FR-007**: Update release scripts and agent context update scripts to support Junie.

### Key Entities
- **Junie Agent**: The AI agent entity being added to the system's configuration.

## Success Criteria

### Measurable Outcomes
- **SC-001**: `specify init --ai junie` creates the expected directory structure.
- **SC-002**: All documentation (README, AGENTS.md, help text) mentions Junie.
- **SC-003**: No regressions in other agent supports.

## Clarifications

### Session 2026-03-12
- Q: Does Junie have a standalone CLI tool that needs to be checked, or is it always environment-based? → A: Environment-based (`requires_cli: False`), as it's the current agent.
- Q: What is the official installation or documentation URL for Junie for `specify check`? → A: `https://github.com/JetBrains/junie` (placeholder, or link to JetBrains Junie docs).
- Q: Should Junie use `.junie/` or another name for its agent folder? → A: `.junie/` is standard and matches the name.
- Q: Should Junie use `commands` as the command subdirectory? → A: Yes, consistent with most other agents.
