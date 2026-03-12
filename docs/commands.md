# Spec-Kit Command Hub

> Spec-Kit implements Spec-Driven Development (SDD) via slash commands.
> Constitution lives at `.specify/memory/constitution.md`.
> Full methodology: `Rules/methodology.md §1`.

## The Four-Phase Workflow

```text
SPECIFY     PLAN        TASKS       IMPLEMENT
   ↓           ↓           ↓           ↓
spec.md   plan.md    tasks.md     code + tests
 What/Why    How       Actions     Execute
```

### Phase 0 - Foundation

| Command | File | Purpose |
|---------|------|---------|
| [`/speckit.constitution`](speckit.constitution.md) | `.specify/memory/constitution.md` | Define non-negotiable principles before any spec work |

### Phase 1 - SPECIFY

| Command | Output | Purpose |
|---------|--------|---------|
| [`/speckit.specify`](speckit.specify.md) | `specs/###-name/spec.md` | Create feature spec from natural language intent |
| [`/speckit.clarify`](speckit.clarify.md) | Annotations on `spec.md` | Resolve ambiguities before planning |
| [`/speckit.checklist`](speckit.checklist.md) | Quality report | Validate requirements quality at any phase |

### Phase 2 - PLAN

| Command | Output | Purpose |
|---------|--------|---------|
| [`/speckit.plan`](speckit.plan.md) | `specs/###-name/plan.md` | Generate technical implementation plan from spec |

### Phase 3 - TASKS

| Command | Output | Purpose |
|---------|--------|---------|
| [`/speckit.tasks`](speckit.tasks.md) | `specs/###-name/tasks.md` | Create dependency-ordered task breakdown |

### Phase 4 - IMPLEMENT

| Command | Purpose |
|---------|---------|
| [`/speckit.implement`](speckit.implement.md) | Execute tasks from `tasks.md` following TDD |
| [`/speckit.analyze`](speckit.analyze.md) | Cross-artifact consistency check before implementation |

---

## npm Aliases

Run Spec-Kit phases via npm scripts (shortcuts to Cline prompts):

```bash
npm run speckit:constitution   # Phase 0 - constitution setup
npm run speckit:specify        # Phase 1 - feature specification
npm run speckit:plan           # Phase 2 - implementation plan
npm run speckit:tasks          # Phase 3 - task breakdown
npm run speckit:implement      # Phase 4 - implementation
```

---

## File Structure

```text
project/
├── .specify/memory/constitution.md    # Non-negotiable principles
└── specs/
    └── 001-feature-name/
        ├── spec.md        # What & why (Phase 1)
        ├── plan.md        # How (Phase 2)
        └── tasks.md       # Action items (Phase 3)
```

---

## Decision Tree

```text
New project?          → Start with /speckit.constitution
New feature?          → /speckit.specify → /speckit.clarify → /speckit.plan
Ready to build?       → /speckit.tasks → /speckit.implement
Quality check?        → /speckit.checklist (any phase)
Pre-impl validation?  → /speckit.analyze
```

---

## Integration with satware AG

| Spec-Kit Artifact | satware AG Equivalent |
|-------------------|-----------------------|
| Constitution | `Rules/*.md` |
| Specification | `docs/product/project-brief.md` |
| Plan | `docs/adr/` |
| Tasks | GitLab Issues (`spec::` label) |
| Implement | Baby Steps™ (<200 LOC/commit) |

**Full SDD overview**: [spec-driven-development.md](spec-driven-development.md)
**Methodology reference**: `Rules/methodology.md §1`
