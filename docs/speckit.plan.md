# /speckit.plan

Generate a technical implementation plan from the specification.

## Purpose
The `/speckit.plan` command translates the feature specification into a detailed technical plan, mapping business requirements to technical architecture.

## Output
- `specs/###-name/plan.md`

## Usage
Run this command once the feature specification is stable.

```bash
/speckit.plan [specification file path or context]
```

## Workflow
1. **Spec Analysis**: Reads the feature requirements and acceptance criteria.
2. **Constitutional Check**: Ensures the technical decisions align with project principles.
3. **Architecture**: Defines technical decisions, data models, and API contracts.
4. **Validation Guide**: Generates a quickstart guide capturing key validation scenarios.
