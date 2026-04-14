# Implementation Plan - Optimize Spec Kit for satware AI Ecosystem

[Overview]
Optimize the GitHub Spec Kit to integrate seamlessly with satware's global AI agent configuration (Rules, Workflows, Skills, Hooks) and add first-class support for the Hermes agent.

The current Spec Kit provides basic bootstrapping for various agents but lacks deep integration with the 2026 satware standards defined in `~/Documents/Cline`. This plan outlines the adding of Hermes agent support, implementing a "sync-not-copy" philosophy for global rules, and refining `/speckit.*` prompts to enforce Baby Steps™ and Half-Token methodologies.

[Types]
Enhance the internal `AGENT_CONFIG` data structure to support Hermes and its specific directory conventions.

- Update `AGENT_CONFIG` in `src/specify_cli/__init__.py` to include `hermes` with `folder: ".hermes/"` and `commands_subdir: "commands"`.

[Files]
Update configuration, scripts, and templates to support the new agent and global sync logic.

Detailed breakdown:
- **src/specify_cli/__init__.py**: Modify to add `hermes` agent configuration and update CLI help text.
- **scripts/bash/update-agent-context.sh**: Rewrite the core logic to detect `~/Documents/Cline` and update project-local rules/skills by referencing the global source.
- **templates/commands/*.md**: Update all prompt templates (specify, plan, clarify, tasks, implement) to inject satware-specific instructions.
- **AGENTS.md**: Update documentation to reflect Hermes support and the global sync architecture.
- **templates/agent-file-template.md**: Refine to align with satware's persona and methodology standards.

[Functions]
Update the CLI entry point and help builders.

Detailed breakdown:
- **_build_ai_assistant_help** (src/specify_cli/__init__.py): Ensure the new `hermes` agent is listed in the dynamic help text.
- **update_agent_file** (scripts/bash/update-agent-context.sh): Modify to check for the existence of `~/Documents/Cline` and perform updates based on global Rules.

[Classes]
No new classes required; modifications are focused on configuration dicts and shell logic.

[Dependencies]
No new Python or system dependencies required. The implementation relies on existing `typer` and standard Linux/macOS CLI tools.

[Implementation Order]
1.  **Add Hermes Support**: Update `AGENT_CONFIG` and help text in the Python core.
2.  **Implement Global Sync Logic**: Update `update-agent-context.sh` to handle `~/Documents/Cline` references and the Hermes-specific file path (`.hermes.md` or `AGENTS.md`).
3.  **Refine Prompt Templates**: Inject satware methodology (Baby Steps™, Half-Token, QCR) into the command templates.
4.  **Update Documentation**: Ensure `AGENTS.md` and `README.md` reflect the optimizations.

task_progress Items:
- [ ] Step 1: Update src/specify_cli/__init__.py with Hermes agent config
- [ ] Step 2: Update scripts/bash/update-agent-context.sh for global sync and Hermes support
- [ ] Step 3: Refine templates/commands/*.md with satware methodology logic
- [ ] Step 4: Update templates/agent-file-template.md and global AGENTS.md
- [ ] Step 5: Verify optimization with a test run of `specify init`
