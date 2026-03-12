# Tasks: Add Junie Agent Support

## Phase 1: Foundational
- [ ] T001 [P] Identify all files needing updates based on AGENTS.md guidelines specs/001-add-junie-agent/plan.md

## Phase 2: Implementation - Junie Agent Support
- [ ] T002 [US1] Add `junie` to `AGENT_CONFIG` in `src/specify_cli/__init__.py`
- [ ] T003 [US1] Update `ai_assistant` option help text in `src/specify_cli/__init__.py`
- [ ] T004 [US1] Update `README.md` Supported AI Agents table
- [ ] T005 [US1] Update `AGENTS.md` Current Supported Agents and Step-by-Step guide
- [ ] T006 [US1] Update `.github/workflows/scripts/create-release-packages.sh` (ALL_AGENTS and case statement)
- [ ] T007 [US1] Update `scripts/bash/update-agent-context.sh` for Junie support
- [ ] T008 [US1] Update `scripts/powershell/update-agent-context.ps1` for Junie support
- [ ] T009 [US1] Update `.github/workflows/scripts/create-github-release.sh` to include Junie packages

## Phase 3: Verification
- [ ] T010 [US1] Verify `specify init --here --ai junie` creates `.junie/commands/`
- [ ] T011 [US1] Verify that documentation changes are correct and visible
