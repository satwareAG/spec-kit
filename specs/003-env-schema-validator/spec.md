---
description: Environment schema validator addon - generates .env.schema from spec constraints.
tags: [env, schema, validation, secrets, sdd]
priority: P1
created: 2026-04-14
---

# Spec: Environment Schema Validator (`/speckit.env-schema`)

## Summary

Generate a `.env.schema` file from spec artifacts declaring all environment variables with types, defaults, secret patterns, and `_ref` bindings for deployment validation.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | Extract env vars from spec.md, plan.md, tasks.md | Must |
| FR-002 | Generate .env.schema JSON with type, required, default, secret fields | Must |
| FR-003 | Support _ref pattern for secrets (env:VAR, vault:path) | Must |
| FR-004 | Generate safe .env.example without real secret values | Must |

## Success Criteria

- /speckit.env-schema produces valid .env.schema JSON
- Secrets never contain literal values
- .env.example is safe to commit

## Command Template

Located at: `templates/commands/env-schema.md`