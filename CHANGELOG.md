# Changelog

<!-- insert new changelog below this comment -->

## [satware-0.8.0] - 2026-04-24

### Changed

- chore: sync fork with upstream v0.8.0

## [0.8.0] - 2026-04-23

### Changed

- feat(presets): Composition strategies (prepend, append, wrap) for templates, commands, and scripts (#2133)
- feat(copilot): support `--integration-options="--skills"` for skills-based scaffolding (#2324)
- docs(install): add pipx as alternative installation method (#2288)
- Add Memory MD community extension (#2327)
- Update version-guard to v1.2.0 (#2321)
- fix: `--force` now overwrites shared infra files during init and upgrade (#2320)
- chore: release 0.7.5, begin 0.7.6.dev0 development (#2322)

## [satware-0.7.3+1] - 2026-04-20

### Changed

- chore: sync fork with upstream v0.7.3; accept upstream's marker-based context upsert (replacing shell-based `update-context.*` scripts) and verify all fork-only agents (agy, bob, iflow, kimi, hermes, cline) set `context_file` correctly

## [0.7.5] - 2026-04-22

### Changed

- fix: resolve skill placeholders for all SKILL.md agents, not just codex/kimi (#2313)
- feat(cli): add specify self check and self upgrade stub (#2316)
- Update version-guard to v1.1.0 (#2318)
- docs: move community presets from README to docs/community (#2314)
- catalog: add wireframe extension (v0.1.1) (#2262)
- Move community walkthroughs from README to docs/community (#2312)
- docs(readme): list red-team in community-extensions table (#2311)
- feat(catalog): add red-team extension to community catalog (#2306)
- Add superpowers-bridge community extension (#2309)
- feat: implement preset wrap strategy (#2189)
- fix(agents): block directory traversal in command write paths (#2229) (#2296)
- chore: release 0.7.4, begin 0.7.5.dev0 development (#2299)

## [0.7.4] - 2026-04-21

### Changed

- fix(copilot): use --yolo to grant all permissions in non-interactive mode (#2298)
- feat: add CITATION.cff and .zenodo.json for academic citation support (#2291)
- Add spec-validate to community catalog (#2274)
- feat: register Ripple in community catalog (#2272)
- Add version-guard to community catalog (#2286)
- Add spec-reference-loader to community catalog (#2285)
- Add memory-loader to community catalog (#2284)
- fix(integrations): strip UTF-8 BOM when reading agent context files (#2283)
- Preset fiction book writing1.6 (#2270)
- fix(integrations): migrate Antigravity (agy) layout to .agents/ and deprecate --skills (#2276)
- chore: release 0.7.3, begin 0.7.4.dev0 development (#2263)

## [0.7.3] - 2026-04-17

### Changed

- fix: replace shell-based context updates with marker-based upsert (#2259)
- Add Community Friends page to docs site (#2261)
- Add Spec Scope extension to community catalog (#2172)
- docs: add Community-maintained plugin for Claude Code and GitHub Copilot CLI that installs Spec Kit skills via the plugin marketplace to README (#2250)
- fix: suppress CRLF warnings in auto-commit.ps1 (#2258)
- feat: register Blueprint in community catalog (#2252)
- preset: Update preset-fiction-book-writing to community catalog -> v1.5.0 (#2256)
- chore(deps): bump actions/upload-pages-artifact from 3 to 5 (#2251)
- fix: add reference/*.md to docfx content glob (#2248)
- chore: release 0.7.2, begin 0.7.3.dev0 development (#2247)

## [0.7.2] - 2026-04-16

### Changed

- docs: add core commands reference and simplify README CLI section (#2245)
- docs: add workflows reference, reorganize into docs/reference/, and add --version flag (#2244)
- docs: add presets reference page and rename pack_id to preset_id (#2243)
- docs: add extensions reference page and integrations FAQ (#2242)
- docs: consolidate integration documentation into docs/integrations.md (#2241)
- feat: update memorylint and superpowers-bridge versions to 1.3.0 with new download URLs (#2240)
- feat: Integration catalog — discovery, versioning, and community distribution (#2130)
- Add Catalog CI extension to community catalog (#2239)
- Added issues extension (#2194)
- chore: release 0.7.1, begin 0.7.2.dev0 development (#2235)

## [0.7.1] - 2026-04-15

### Changed

- ci: add windows-latest to test matrix (#2233)
- docs: remove deprecated --skip-tls references from local-development guide (#2231)
- fix: allow Claude to chain skills for hook execution (#2227)
- docs: merge TESTING.md into CONTRIBUTING.md, remove TESTING.md (#2228)
- Add agent-assign extension to community catalog (#2030)
- fix: unofficial PyPI warning (#1982) and legacy extension command name auto-correction (#2017) (#2027)
- feat: register architect-preview in community catalog (#2214)
- chore: deprecate --ai flag in favor of --integration on specify init (#2218)
- chore: release 0.7.0, begin 0.7.1.dev0 development (#2217)
