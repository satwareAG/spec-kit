# /speckit.constitution

Define non-negotiable principles before any spec work.

## Purpose
The `/speckit.constitution` command is used to initialize or update the project's constitution. This document serves as the foundation for all subsequent development, defining the core principles and rules that must be followed.

## File
- Output: `.specify/memory/constitution.md`

## Usage
Run this command at the beginning of a new project or when project-wide principles need to be updated.

```bash
/speckit.constitution [principles or project details]
```

## Workflow
1. **Initialize**: If the constitution doesn't exist, it's created from a template.
2. **Collect**: The agent gathers principles from user input or project context.
3. **Fill**: Placeholders in the template are replaced with concrete values.
4. **Propagate**: Changes are synchronized across other templates (plan, spec, tasks).
5. **Report**: A sync impact report is generated.
