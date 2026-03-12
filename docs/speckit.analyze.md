# /speckit.analyze

Cross-artifact consistency check before implementation.

## Purpose
The `/speckit.analyze` command validates the alignment between `spec.md`, `plan.md`, and `tasks.md` before implementation begins. It ensures that no requirements were lost and that the technical decisions and tasks fully support the specification.

## Usage
Run this command after all specification and planning artifacts are complete but before starting implementation.

```bash
/speckit.analyze [path to spec, plan, or tasks]
```

## Workflow
1. **Consistency Analysis**: Cross-references requirements from `spec.md` with technical decisions in `plan.md` and actions in `tasks.md`.
2. **Gaps & Conflicts**: Identifies any missing requirements, conflicting technical choices, or out-of-order tasks.
3. **Alignment Report**: Produces a summary report of findings and necessary refinements.
