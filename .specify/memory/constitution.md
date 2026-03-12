<!--
Sync Impact Report:
Version change: [INITIAL] -> 1.0.0
List of modified principles:
- I. Library-First (added)
- II. CLI Interface (added)
- III. Test-First (added)
- IV. Simplicity (added)
- V. Anti-Abstraction (added)
Added sections: Core Principles, Technical Context, Governance
Templates requiring updates:
- .specify/templates/plan-template.md (✅ updated)
- .specify/templates/spec-template.md (✅ updated)
- .specify/templates/tasks-template.md (✅ updated)
Follow-up TODOs: None
-->

# Spec-Kit Constitution

## Core Principles

### I. Library-First
Every feature starts as a standalone library. Libraries must be self-contained, independently testable, and documented. There should be a clear purpose for every library - no organizational-only libraries.

### II. CLI Interface
Every library exposes functionality via a CLI. We use a text in/out protocol: stdin/args → stdout, and errors → stderr. We support both JSON and human-readable formats to ensure both machine and human interoperability.

### III. Test-First (NON-NEGOTIABLE)
TDD is mandatory. Tests must be written and verified to fail before implementation begins. The Red-Green-Refactor cycle is strictly enforced. No code should be merged without accompanying tests that cover the new functionality.

### IV. Simplicity
We value simplicity over complexity. Maximize the amount of work not done. We avoid future-proofing and over-engineering. If a feature is not needed now, it is not implemented.

### V. Anti-Abstraction
Use frameworks and libraries directly rather than creating custom wrappers. We prefer a single model representation and avoid unnecessary layers of abstraction that increase cognitive load without adding clear value.

## Technical Context
The project is built using Python, focusing on providing a toolkit for Spec-Driven Development. It includes the `specify` CLI and various templates for SDD.

## Governance
This constitution supersedes all other practices within the Spec-Kit project. Amendments to this constitution require documentation, approval, and a migration plan if existing features are affected. All pull requests and code reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-03-12 | **Last Amended**: 2026-03-12
