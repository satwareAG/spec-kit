# /speckit.tasks

Create a dependency-ordered task breakdown.

## Purpose
The `/speckit.tasks` command analyzes the implementation plan and related design documents to generate a structured, executable task list.

## Output
- `specs/###-name/tasks.md`

## Usage
Run this command once the technical plan is finalized and you're ready to start development.

```bash
/speckit.tasks [plan file path or context]
```

## Workflow
1. **Inputs**: Analyzes `plan.md` and related documents (data-model, contracts).
2. **Task Derivation**: Converts technical decisions and scenarios into actionable tasks.
3. **Parallelization**: Identifies independent tasks that can be performed in parallel.
4. **Ordering**: Arranges tasks in a dependency-ordered sequence.
