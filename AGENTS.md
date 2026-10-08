# AGENTS.md

## About Spec Kit and Specify

**GitHub Spec Kit** is a comprehensive toolkit for implementing Spec-Driven Development (SDD) - a methodology that emphasizes creating clear specifications before implementation. The toolkit includes templates, scripts, and workflows that guide development teams through a structured approach to building software.

**Specify CLI** is the command-line interface that bootstraps projects with the Spec Kit framework. It sets up the necessary directory structures, templates, and AI agent integrations to support the Spec-Driven Development workflow.

The toolkit supports multiple AI coding assistants, allowing teams to use their preferred tools while maintaining consistent project structure and development practices.

## Adding or Updating CLI Commands

Before adding, updating, or reorganizing Specify CLI commands, read
[Shared Command Application Architecture](design/shared.md) and
[Specify CLI Command Architecture](design/cli.md). They define the shared
operation boundary, command-module naming, private phases, nested command
groups, registration ownership, and mirrored tests.

## Adding or Updating MCP Commands

Before adding or changing MCP tools for Specify commands, read
[Shared Command Application Architecture](design/shared.md) and
[Specify MCP Command Architecture](design/mcp.md). They define the shared
operation boundary, typed contracts, explicit inventory, side-effect metadata,
the local stdio protocol boundary, and mirrored tests.

## Adding or Updating Agent Integrations

Before adding or changing AI agent integrations, read
[Agent Integration Design](design/integration.md). It covers
delivery routes, output formats, registration, and install/uninstall ownership.

## Adding or Updating Workflow Steps

Before adding or changing workflow step types, read
[Workflow Step Design](design/workflow-step.md). It covers registration,
validation, execution, resume, and installed step packages.

## Testing Executable Behavior

Before changing code or configuration that runs or controls execution without
an LLM, read
[Testing deterministic behavior](CONTRIBUTING.md#testing-deterministic-behavior).
Behavioral changes need positive and negative coverage; bug fixes need
before-and-after regression evidence.

## Branches and Agent Contributions

When creating a branch, follow [Branch naming](CONTRIBUTING.md#branch-naming).
Before authoring commits, opening PRs, or posting review comments, read
[Agent-authored Git and review activity](CONTRIBUTING.md#agent-authored-git-and-review-activity).
Agent-authored commits and AI-generated PRs and comments each require their
own disclosure; a PR-body disclosure alone does not cover later activity.

## Other Contribution Guidance

For contribution or repository-workflow questions not covered above, or when
the applicable guidance is unclear, read [CONTRIBUTING.md](CONTRIBUTING.md)
before acting.

## Common Pitfalls

- **Running tests against the wrong environment:** Run the suite inside this
  worktree's own virtualenv (`uv sync --extra test` then
  `.venv/bin/python -m pytest`). A bare `uv run pytest` can pick up an
  editable install from another worktree and fail to import new subpackages.

---

## IPADP Conformance & Cline Harmony

This fork of `spec-kit` participates in the **Inter-Project Agentic Development
Process (IPADP)** as project #6. It targets **L3 conformance** — the highest
level defined in the IPADP RFC.

See: `specs/metadata.json`, `llms.txt`, and the IPADP RFC hosted in the
internal satware AG `wiki` repository (`specs/rfc-interproject-agentic-development.md`).

### Conformance Matrix

| Level | Requirement | Artifact in this repo |
|-------|-------------|-----------------------|
| L1    | `AGENTS.md` + `specs/metadata.json` with upstream/downstream graph | This file + `specs/metadata.json` |
| L2    | Privacy validation in CI                                          | `scripts/bash/check-privacy-leaks.sh`, `.privacy-whitelist`, `.github/workflows/privacy-check.yml` |
| L3    | Automated upstream sync + morning protocol integration            | `scripts/bash/check-upstream-sync.sh`, `.github/workflows/upstream-sync-check.yml`, `scripts/bash/sod.sh`, `scripts/bash/eod.sh`, `scripts/bash/daily-routine.sh`, `$SATWARE_HARNESS/workflows/sod.protocol.md` / `eod.protocol.md` |

### Harmony with the satware harness (`$SATWARE_HARNESS`)

Agents working on this repository MUST follow the global satware AG agent rules
distributed via the harness. The canonical source of truth is
`$SATWARE_HARNESS/rules/`, synchronized into consumer projects via
`$SATWARE_HARNESS/scripts/env-setup-symlinks.sh`. The `SATWARE_HARNESS`
environment variable is exported by `scripts/prepare-env.sh` (run once after
cloning the harness) and persisted to `~/.config/satware/harness.env`.

Key rules that govern SDD/TDD and day-to-day behavior on spec-kit:

- `methodology.core.md` — core SDD/TDD/RLM methodology
- `code.quality.md`     — code quality bar, reviews, refactoring
- `context.management.md` — git-native context and zero-persistence memory
- `agent.framework.md`, `agent.guardrails.md` — operational framework and guardrails
- `ecosystem.ipadp.md`  — IPADP conformance (this is IPADP project #6)
- `release.immutability.md` — tag immutability (governs upstream-sync workflow)
- `code.cross-platform.md` — cross-platform discipline (shell/powershell paths, encodings)

### Morning / EoD Protocol Integration

At the start of every working session an agent working on this repository SHOULD:

1. Run the repo-local SoD hook: `bash scripts/bash/daily-routine.sh sod` (references `$SATWARE_HARNESS/workflows/sod.protocol.md` when available, then runs `check-privacy-leaks.sh` and `check-upstream-sync.sh`).
2. At the end of the session, run the repo-local EoD hook: `bash scripts/bash/daily-routine.sh eod` (references `$SATWARE_HARNESS/workflows/eod.protocol.md` when available, then runs `check-privacy-leaks.sh`).

In CI, `.github/workflows/upstream-sync-check.yml` runs `scripts/bash/check-upstream-sync.sh` on a daily schedule and opens/updates a rolling `upstream-sync: <tag> available` issue when a new upstream `github/spec-kit` release tag is detected.

See `docs/ipadp-l3-automation.md` for full details on the scheduled workflow, the SoD/EoD integration, local run instructions, and failure/override modes.

See `docs/fork-agent-parity.md` for the fork-agent parity audit (IPADP Phase 4.3): required class attributes, inheritance chain, delta vs upstream-bundled integrations, and the regression contract enforced by `tests/integrations/test_fork_agent_parity.py`.

### SDD/TDD Workflow (short form)

1. **Spec first** — create or update a spec under `specs/<feature>/spec.md` using `templates/spec-template.md`.
2. **Plan** — derive `specs/<feature>/plan.md` from `templates/plan-template.md`.
3. **Tasks** — break down into verifiable tasks (`templates/tasks-template.md`).
4. **Test-first** — add failing tests under `tests/` before implementation.
5. **Implement** — make the tests pass with the minimum change set.
6. **Checklists** — fulfill `templates/checklist-template.md` prior to merge.
7. **Privacy + upstream sync** — verify via the two scripts above.
8. **Pre-PR check** — run `bash scripts/bash/daily-routine.sh pre-pr` before pushing to catch lint/test failures locally. Runs ruff, integration tests, privacy check, and upstream sync in a single pass.
9. **Commit + PR** — follow conventional commits (`<type>(<scope>): <msg>`) with signed trailers where required.

---

## Error Handling and Debugging

### Common Errors and Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| `Integration '<key>' not found` | Missing `_register()` call | Add `_register(<Name>Integration())` inside `_register_builtins()` |
| `NameError: name '<Name>Integration' is not defined` at startup | Missing import | Add `from .<package_dir> import <Name>Integration` inside `_register_builtins()` |
| CLI check fails for a `requires_cli: True` agent | `key` does not match the executable name | Set `key` to the exact name `shutil.which(key)` must resolve (e.g. `"cursor-agent"`, not `"cursor"`) |
| Command files have the wrong argument syntax | Wrong `args` value in `registrar_config` | Use `$ARGUMENTS` for Markdown agents, `{{args}}` for TOML/YAML agents, or the agent's custom placeholder |
| `ModuleNotFoundError` on a brand-new subpackage under pytest only | Ambient interpreter with a stale editable `.pth` | Run inside this tree's own venv (see Common Pitfalls) |
| Uninstall leaves files behind, or skips files you expected removed | Files not recorded via the manifest, or their hash changed after install | Route every created file through `manifest.record_file(...)`; user-edited files are intentionally skipped unless `force=True` |
| Context file (`CLAUDE.md`, etc.) not updated | Expecting the CLI to manage it | Context files are owned by the opt-in `agent-context` extension, not the integration — see [Context file behavior](#4-context-file-behavior) |

### Debugging Tips

**Inspect the manifest** to see what an installed integration tracks:

```bash
cat .specify/integrations/<key>.manifest.json
```

**Verify a CLI tool is detected** before debugging a `requires_cli` agent:

```bash
which <key>        # Should print the executable path if installed
```

**Verify the installed output structure** after `specify init`:

```bash
find my-project/<folder> -type f
```

---

## Contribution Checklist

Before opening or merging an integration PR, confirm the following:

- [ ] Added the integration subpackage under `src/specify_cli/integrations/<package_dir>/`.
- [ ] Registered it (import **and** `_register()`) in `src/specify_cli/integrations/__init__.py`, both alphabetical.
- [ ] Added or updated tests in `tests/integrations/test_integration_<key>.py`.
- [ ] Verified the install/uninstall flow with `specify init --integration <key>`.
- [ ] Did **not** add `context_file` handling to the CLI (that belongs to the `agent-context` extension).
- [ ] Updated devcontainer files if the agent needs a VS Code extension or CLI install step.
- [ ] Updated this guide or other relevant docs if the integration has special setup or limitations.

---

*This documentation should be updated whenever new integrations are added to maintain accuracy and completeness.*
