---
description: Taskfile/Makefile generator addon - creates CI/CD orchestration from SDD task breakdowns.
tags: [orchestration, taskfile, makefile, ci-cd, sdd]
priority: P1
created: 2026-04-14
---

# Spec: Taskfile/Makefile Generator (`/speckit.orchestrate`)

## Summary

Generate a Taskfile.yml or Makefile from tasks.md to provide CI/CD-ready orchestration chaining spec-to-code pipeline stages.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Parse tasks.md and extract task IDs, dependencies, and phases | Must |
| FR-002 | Generate Taskfile.yml by default, Makefile as fallback | Must |
| FR-003 | Create standard targets: generate, validate, smoke-test, deploy, lint, test, check | Must |
| FR-004 | Map each task to a sub-target with correct dependency ordering | Must |

## Success Criteria

- Running /speckit.orchestrate produces a valid Taskfile.yml or Makefile
- All tasks from tasks.md appear as targets or dependencies
- Default target runs full pipeline

## Command Template

Located at: `templates/commands/orchestrate.md`