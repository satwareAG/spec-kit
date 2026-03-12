# /speckit.implement

Execute tasks from `tasks.md` following Test-Driven Development (TDD).

## Purpose
The `/speckit.implement` command is the main execution engine of Spec-Kit. It systematically processes the `tasks.md` file, implementing each task with a strict TDD cycle.

## Usage
Run this command when you're ready to start coding.

```bash
/speckit.implement [task file path or specific task IDs]
```

## Workflow
1. **Task Selection**: Picks the next incomplete task from `tasks.md`.
2. **Analysis**: Evaluates the task's context (plan, spec, existing code).
3. **Red-Green-Refactor**: Follows the TDD cycle (write failing test, write minimal code to pass, refactor).
4. **Verification**: Confirms task completion and updates `tasks.md`.
