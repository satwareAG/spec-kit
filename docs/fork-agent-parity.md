# Fork-Agent Parity Audit

IPADP Phase 4.3 (issue #24) — reference documentation and regression contract
for the fork-only AI-agent integrations shipped by `satwareAG/spec-kit`.

## Fork-only agents

| Key | Base class | `context_file` | Requires CLI |
|-----|------------|----------------|--------------|
| `agy` | `SkillsIntegration` | `AGENTS.md` | yes |
| `bob` | `MarkdownIntegration` | `AGENTS.md` | yes |
| `iflow` | `MarkdownIntegration` | `IFLOW.md` | yes |
| `kimi` | `SkillsIntegration` | `KIMI.md` | yes |
| `hermes` | `MarkdownIntegration` | `SOUL.md` | no |
| `cline` | `MarkdownIntegration` | `.cline/rules` | yes |

These agents are **not** present in upstream `github/spec-kit`. Parity with
the upstream `IntegrationBase` contract is enforced automatically; see
*Regression contract* below.

## Required class attributes

Every fork agent subclasses a base class under
`src/specify_cli/integrations/base.py` and must declare:

| Attribute | Type | Purpose |
|-----------|------|---------|
| `key` | `str` | Unique identifier; for `requires_cli: True` must match the executable name. |
| `config` | `dict` | `name`, `folder`, `commands_subdir`, `install_url`, `requires_cli`. |
| `registrar_config` | `dict` | `dir`, `format` (`markdown`/`toml`/`yaml`), `args`, `extension`. |
| `context_file` | `str` | Non-empty path to the agent context/instructions file. |

## Inheritance chain

```
IntegrationBase
├── MarkdownIntegration   ← bob, iflow, hermes, cline
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
2. `integration.key` matches the expected key (agy/bob/iflow/kimi/hermes/cline).
3. `config` contains all required keys with correct types.
4. `registrar_config` contains all required keys and `format` ∈
   `{markdown, toml, yaml}`.
5. `context_file` is a non-empty string.
6. End-to-end: `specify init --here --integration <key> --script sh` exits 0
   and produces at least one file under the configured commands directory
   (`registrar_config["dir"]`).

This gives **36 parametrised assertions** across the 6 fork agents. Any
upstream change that silently breaks the `IntegrationBase` contract for fork
agents will now fail this test before it reaches `main-speck`.

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
