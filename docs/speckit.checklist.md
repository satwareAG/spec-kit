# /speckit.checklist

Validate requirements quality at any phase.

## Purpose
The `/speckit.checklist` command produces a quality report on requirements, ensuring they meet project-wide and standard quality criteria.

## Output
- Quality report (usually in `specs/###-name/checklists/`)

## Usage
Run this command periodically at any phase to validate the current artifact's quality.

```bash
/speckit.checklist [artifact to check]
```

## Workflow
1. **Criteria Collection**: Gathers quality criteria from the project constitution.
2. **Analysis**: Evaluates the target artifact (spec, plan, tasks) against the criteria.
3. **Reporting**: Generates a detailed quality report.
