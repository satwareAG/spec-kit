# /speckit.specify

Create a feature specification from natural language intent.

## Purpose
The `/speckit.specify` command transforms a simple feature description (the user-prompt) into a complete, structured specification. It also handles automatic feature numbering and branch creation.

## Output
- `specs/###-name/spec.md`

## Usage
Run this command when you have a new feature idea or change request.

```bash
/speckit.specify [feature description]
```

## Workflow
1. **Short Name & Branch**: Generates a semantic branch name and creates it.
2. **Feature Numbering**: Automatically assigns the next sequential number.
3. **Template**: Uses a specification template to structure the feature requirements.
4. **Content Generation**: Translates intent into actors, actions, data, and constraints.
5. **Quality Checklist**: Generates a quality checklist for the specification.
