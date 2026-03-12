# Implementation Plan: Add Junie Agent Support

## Technical Context
- Tech Stack: Python (Specify CLI), Shell scripts (Bash/PowerShell).
- Dependencies: `specify-cli` (the current project), `typer`, `rich`.

## Constitution Check
- [x] Principle I: Library-First - The changes are within the `specify_cli` library.
- [x] Principle II: CLI Interface - This feature enhances the CLI interface.
- [x] Principle III: Test-First - Tests will be added before implementation.
- [x] Principle IV: Simplicity - Adding an agent is a straightforward addition to an existing configuration.
- [x] Principle V: Anti-Abstraction - We add the agent directly to the configuration dictionary as per existing patterns.

## Architecture
We will follow the existing pattern for adding agents as defined in `src/specify_cli/__init__.py`'s `AGENT_CONFIG`.
The `init` command automatically handles agent folder creation and template extraction based on this config.

## Data Model
- **Junie Agent Config**:
  - `name`: "Junie"
  - `folder`: ".junie/"
  - `commands_subdir`: "commands"
  - `install_url`: "https://github.com/JetBrains/junie"
  - `requires_cli`: False

## Contracts
The contract is the `AGENT_CONFIG` dictionary structure and the `specify init` CLI options.

### `specify init` --ai option
- Added choice: `junie`

## Research
- **Decision**: Use `junie` as the key.
- **Rationale**: Matches the agent's name and follows the pattern of other agents like `copilot` and `roo`.
- **Alternatives considered**: `jetbrains-junie`, `junie-agent`. `junie` is the simplest and most direct.

## Quickstart
1. `specify init . --ai junie`
2. `ls -la .junie/commands/`
