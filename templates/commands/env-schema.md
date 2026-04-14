---
description: Generate .env.schema from spec constraints to validate required/optional environment variables, types, defaults, and secret patterns before deployment.
handoffs:
  - label: Generate Orchestration
    agent: speckit.orchestrate
    prompt: Generate Taskfile or Makefile orchestration for the project
  - label: Implement Tasks
    agent: speckit.implement
    prompt: Begin implementing environment schema validation
---

## User Input

```text
$ARGUMENTS
```

## Task

Generate a **`.env.schema`** file from the project's specification artifacts. This file declares all environment variables needed by the project, derived from functional requirements, technical constraints, and deployment configuration.

## Execution Flow

1. **Detect Project Context**:
   - Read `specs/*/spec.md` for functional requirements referencing configuration
   - Read `specs/*/plan.md` for technical architecture and infrastructure references
   - Read `specs/*/tasks.md` for implementation-level env var usage
   - Read `.specify/memory/constitution.md` for security and compliance standards

2. **Extract Environment Variables** from spec artifacts:
   - **FR references**: Any functional requirement mentioning configuration (`DATABASE_URL`, `API_KEY`, etc.)
   - **TC thresholds**: Performance/test thresholds (`MAX_CONNECTIONS`, `TIMEOUT_MS`)
   - **Deployment config**: Infrastructure variables from plan.md deployment section
   - **Secret patterns**: Variables requiring secure storage (API keys, tokens, passwords)

3. **Generate `.env.schema`** with the following structure:

   ```json
   {
     "$schema": "https://spec-kit.github.io/schemas/env-schema/v1",
     "version": "1.0.0",
     "generated_from": "specs/001-feature-name/spec.md",
     "variables": {
       "DATABASE_URL": {
         "required": true,
         "type": "string",
         "pattern": "^(postgresql|mysql|sqlite)://.*",
         "description": "Primary database connection string",
         "secret": false,
         "source": "FR-003"
       },
       "API_KEY": {
         "required": true,
         "type": "string",
         "pattern": "^[a-zA-Z0-9]{32,}$",
         "description": "External API authentication key",
         "secret": true,
         "_ref": "env:API_KEY",
         "source": "FR-007"
       },
       "LOG_LEVEL": {
         "required": false,
         "type": "enum",
         "values": ["debug", "info", "warn", "error"],
         "default": "info",
         "description": "Application logging verbosity",
         "secret": false,
         "source": "plan.md:observability"
       },
       "MAX_CONNECTIONS": {
         "required": false,
         "type": "integer",
         "minimum": 1,
         "maximum": 1000,
         "default": 100,
         "description": "Maximum database connection pool size",
         "secret": false,
         "source": "TC-002"
       }
     }
   }
   ```

4. **Secret Reference Pattern (`_ref`)**: For variables marked `secret: true`:
   - Default: `_ref: "env:VAR_NAME"` (read from environment)
   - If vault integration detected in plan: `_ref: "vault:secret/path#field"`
   - If `.env.local` exists: Note it as the expected source
   - Never include actual secret values in the schema

5. **Generate `.env.example`**: Create a safe-to-commit `.env.example` file:
   ```bash
   # Generated from .env.schema - DO NOT edit manually
   # Run /speckit.env-schema to regenerate
   
   # Required
   DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
   API_KEY=your-api-key-here
   
   # Optional (defaults shown)
   LOG_LEVEL=info
   MAX_CONNECTIONS=100
   ```

6. **Validation Report**: Print a summary:
   - Total variables: N
   - Required: N / Optional: N
   - Secrets: N (with `_ref` bindings)
   - Missing from current `.env`: N (if `.env` exists)

## Variable Type System

| Type | Validation | Example |
|------|-----------|---------|
| `string` | Any non-empty string | `APP_NAME` |
| `integer` | Numeric with optional min/max | `PORT` |
| `enum` | Must match one of `values` | `LOG_LEVEL` |
| `boolean` | `true`/`false`/`1`/`0` | `DEBUG` |
| `url` | Valid URL pattern | `DATABASE_URL` |
| `path` | Valid filesystem path | `DATA_DIR` |

## Secret Handling Rules

- Variables with `secret: true` are NEVER written to `.env.example` with real values
- Placeholder values use descriptive text (`your-api-key-here`, `changeme`)
- `_ref` field declares where the runtime value comes from
- Validation fails if a secret variable has no `_ref` and no default source

## Quality Checks

- [ ] All FR-referenced configuration is captured as variables
- [ ] Every variable has a `source` traceable to spec/plan/task
- [ ] Secrets have `_ref` bindings, never literal values
- [ ] `.env.example` is safe to commit (no real secrets)
- [ ] Type constraints are specific enough for automated validation
- [ ] Defaults align with constitution standards (security, performance)