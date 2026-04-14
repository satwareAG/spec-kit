---
description: Generate Taskfile.yml or Makefile orchestration from tasks.md to automate spec-to-code pipelines.
handoffs:
  - label: Validate Environment Schema
    agent: speckit.env-schema
    prompt: Generate environment schema validation for the project
  - label: Implement Tasks
    agent: speckit.implement
    prompt: Begin implementing the orchestrated tasks
---

## User Input

```text
$ARGUMENTS
```

## Task

Generate a **Taskfile.yml** (preferred) or **Makefile** orchestration file from the current project's `tasks.md`. This creates a CI/CD-ready entrypoint that chains spec-to-code pipeline stages.

## Execution Flow

1. **Detect Project Context**:
   - Read `.specify/memory/constitution.md` for project principles
   - Read `specs/*/spec.md` for active specifications
   - Read `specs/*/plan.md` for technical plans
   - Read `specs/*/tasks.md` for task breakdowns

2. **Detect Orchestration Format**:
   - If user specifies `taskfile` or `makefile`, use that format
   - Default: **Taskfile.yml** (modern, YAML-native, better for SDD)
   - Fallback to Makefile if `task` CLI is not available

3. **Parse tasks.md** for task groups, dependencies, and phases

4. **Generate Standard Targets**:

   | Target | Purpose | Source |
   |--------|---------|--------|
   | `generate` | Generate code from specs | `spec.md` → `plan.md` → `tasks.md` |
   | `validate` | Validate specs & generated artifacts | All spec artifacts |
   | `smoke-test` | Run smoke tests from BDD scenarios | `spec.md` acceptance criteria |
   | `deploy` | Deploy validated artifacts | `plan.md` deployment section |
   | `lint` | Run linters & formatters | Constitution standards |
   | `test` | Run full test suite | Task test requirements |
   | `check` | Pre-commit quality gate | All of the above (fast) |

5. **Map Tasks to Targets**: Each task in `tasks.md` becomes a sub-target or dependency:
   - Extract task IDs (T001, T002, etc.)
   - Map dependencies between tasks
   - Group by phase (setup, implement, test, deploy)

6. **Write Orchestration File**:

   **Taskfile.yml** pattern:
   ```yaml
   version: '3'
   vars:
     SPEC_DIR: specs
     SPEC_KIT_VERSION: latest
   
   tasks:
     generate:
       desc: "Generate code from specifications"
       deps: [validate]
       cmds:
         - echo "Generating from {{.SPEC_DIR}}..."
     
     validate:
       desc: "Validate specification artifacts"
       cmds:
         - echo "Validating specs..."
     
     smoke-test:
       desc: "Run smoke tests from BDD scenarios"
       deps: [generate]
       cmds:
         - echo "Running smoke tests..."
     
     deploy:
       desc: "Deploy validated artifacts"
       deps: [smoke-test]
       cmds:
         - echo "Deploying..."
   ```

   **Makefile** pattern (if preferred):
   ```makefile
   .PHONY: generate validate smoke-test deploy lint test check
   
   generate: validate
   	@echo "Generating from specs..."
   
   validate:
   	@echo "Validating specs..."
   
   smoke-test: generate
   	@echo "Running smoke tests..."
   ```

7. **Add SDD Integration**: Include commands that integrate with spec-kit:
   - `task spec-validate` - Validate all spec artifacts exist and are consistent
   - `task spec-checklist` - Run quality checklists
   - `task spec-smoke` - Generate and run smoke tests from BDD scenarios

8. **Report**: Print generated file path, number of targets, and dependency graph.

## Guidelines

- **Idempotent**: Re-running overwrites the orchestration file (never appends)
- **Platform-aware**: Detect OS for shell compatibility (bash vs PowerShell)
- **Incremental**: Only regenerate if `tasks.md` changed since last generation
- **Constitution-aware**: Respect testing coverage thresholds and linting standards from constitution

## Quality Checks

- [ ] All tasks from `tasks.md` are represented as targets or dependencies
- [ ] Dependency graph has no cycles
- [ ] Default target runs the full pipeline (`task` or `make` with no args)
- [ ] Each target has a `desc` (Taskfile) or comment (Makefile)
</task_progress>- [x] Explore codebase - reading key files
- [x] Create `/spec.orchestrate` command template
- [ ] Create spec for P1: Taskfile/Makefile Generator (specs/002-taskfile-generator/)
- [ ] Create `/spec.env-schema` command template
- [ ] Create spec for P1: Environment Schema Validator (specs/003-env-schema-validator/)
- [ ] Update SKILL_DESCRIPTIONS in __init__.py
- [ ] Update CHANGELOG.md and README.md
- [ ] Write tests for both addons
- [ ] Run full test suite and verify</task_progress></write_to_file>