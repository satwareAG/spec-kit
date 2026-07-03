# Fork-Agent Parity Audit

IPADP Phase 4.3 (issue #24) — reference documentation and regression contract
for the fork-only AI-agent integrations shipped by `satwareAG/spec-kit`.

## Fork-only agents

| Key | Base class | Requires CLI |
|-----|------------|--------------|
| `agy` | `SkillsIntegration` | yes |
| `bob` | `MarkdownIntegration` | yes |
| `kimi` | `SkillsIntegration` | yes |
| `hermes` | `MarkdownIntegration` | no |
| `cline` | `MarkdownIntegration` | yes |

These agents were originated by this fork and accepted into upstream
`github/spec-kit` by v0.11.8. They remain registered here as regression
coverage for the fork's contribution; parity with the upstream
`IntegrationBase` contract is enforced automatically (see *Regression
contract* below).

> **No `context_file` column.** Since v0.12.0 (PR #3097) the agent-context
> extension is a full opt-in and owns all context-file knowledge via
> `extensions/agent-context/agent-context-defaults.json`. Integration classes
> no longer declare `context_file` (AGENTS.md pitfall #2).

### Retired fork-originated agents

The following fork-originated agents were retired by upstream after v0.11.8.
The fork follows upstream retirement and drops them in `sync/upstream-v0.12.4`:

| Key | Retired in | Upstream reason |
|-----|-----------|-----------------|
| `iflow` | v0.12.2 (#3166, #3211) | product discontinued |
| `windsurf` | v0.12.2 (#3168, #3213) | absorbed into Cognition Devin |
| `roo` | v0.12.3 (#3167, #3212) | extension shut down |

`windsurf` and `roo` were never tracked by this parity module (not
fork-originated); `iflow` was tracked and has been removed from
`FORK_AGENTS` in `tests/integrations/test_fork_agent_parity.py`.

## Required class attributes

Every fork agent subclasses a base class under
`src/specify_cli/integrations/base.py` and must declare:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `key` | `str` | Unique identifier; for `requires_cli: True` must match the executable name. |
| `config` | `dict` | `name`, `folder`, `commands_subdir`, `install_url`, `requires_cli`. |
| `registrar_config` | `dict` | `dir`, `format` (`markdown`/`toml`/`yaml`), `args`, `extension`. |

> **No `context_file` row.** See the note under *Fork-only agents* above:
> the agent-context extension owns context-file knowledge since v0.12.0.

## Inheritance chain

```
IntegrationBase
├── MarkdownIntegration   ← bob, hermes, cline
├── TomlIntegration
├── YamlIntegration
└── SkillsIntegration     ← agy, kimi
```

Fork agents use **zero custom `setup()` overrides** — all rely on the base
classes' standard template processing. Context-file upkeep is handled by the
marker-based upsert in `base.py` introduced upstream in v0.7.3 (PR #2259):
fork agents do not ship per-integration `update-context.{sh,ps1}` wrappers.

## Delta vs upstream-bundled integrations

| Dimension | Upstream (`claude`, `gemini`, …) | Fork (`agy`, `bob`, …) |
|-----------|----------------------------------|------------------------|
| Base classes used | All four (incl. custom `IntegrationBase` for Copilot) | `MarkdownIntegration`, `SkillsIntegration` only |
| Custom `setup()` overrides | Copilot, Forge | none |
| `options()` overrides | Codex (`--skills`), Copilot, Forge | agy, kimi (`--skills` via `SkillsIntegration`) |
| Context-update mechanism | `base.py` marker-upsert | same (inherited) |

## Regression contract

The test module `tests/integrations/test_fork_agent_parity.py` asserts, for
each fork agent, that:

1. The integration is registered in `INTEGRATION_REGISTRY`.
2. `integration.key` matches the expected key (agy/bob/kimi/hermes/cline).
3. `config` contains all required keys with correct types.
4. `registrar_config` contains all required keys and `format` ∈
   `{markdown, toml, yaml}`.
5. End-to-end: `specify init --here --integration <key> --script sh` exits 0
   and produces at least one file under the configured commands directory
   (`registrar_config["dir"]`).

This gives **25 parametrised assertions** across the 5 fork agents (5 tests ×
5 agents; the former `context_file` assertion was dropped after v0.12.0 made
`context_file` an extension-owned concern). Any upstream change that silently
breaks the `IntegrationBase` contract for fork agents will now fail this test
before it reaches `main-speck`.

## Operational runbook

- When upstream `github/spec-kit` publishes a new release tag, the scheduled
  workflow `.github/workflows/upstream-sync-check.yml` opens/updates a rolling
  tracking issue; the companion workflow
  `.github/workflows/upstream-tag-regression.yml` (IPADP Phase 4.1, issue #22)
  dry-merges the tag and runs the full integration test suite — including this
  parity module — to detect fork-agent breakage **before** a human starts the
  sync.
- On parity failure the remediation is always one of:
  1. Add the missing attribute to the fork agent's `__init__.py`.
  2. Adjust the fork agent's base class if upstream changed the contract.
  3. If upstream has split/renamed a base class, re-pick the appropriate
     subclass and migrate.

See also:
- `AGENTS.md` — overall integration architecture and adding-new-integration guide.
- `docs/ipadp-l3-automation.md` — upstream-sync + SoD/EoD automation layer.
