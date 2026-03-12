# /speckit.clarify

Resolve ambiguities before planning.

## Purpose
The `/speckit.clarify` command analyzes the current `spec.md` for gaps and generates annotations to resolve ambiguities.

## Output
- Annotations on `specs/###-name/spec.md`

## Usage
Run this command after generating a spec but before planning if the requirements are still unclear.

```bash
/speckit.clarify [specific questions or general request]
```

## Workflow
1. **Analysis**: Evaluates the specification for completeness and clarity.
2. **Annotation**: Adds `[NEEDS CLARIFICATION]` markers to the spec.
3. **Dialogue**: Engages in a conversation with the user to refine details.
