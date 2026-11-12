# ui-verify preset (staging)

Conditional UI-VERIFY template additions for Spec Kit: a `UI Surface`
declaration field with browser-drive acceptance guidance (spec template), a
conditional `UI Verification` task section with a findings contract and
checkpoint-blocking UI-VERIFY tasks (tasks template, generated ONLY when the
spec declares a UI surface), and a `UI Requirements Quality` checklist
category (requirement-quality items only).

Non-UI features are unaffected: every addition is conditional
(`*(include if ...)*` / `ONLY if ...`), so generation for API/backend-only
features is unchanged.

## Status: vehicle-neutral staging

The template content is extracted verbatim from satwareAG/spec-kit PR #193
(commit `2cd7871a`), proposed upstream via
[github/spec-kit#5387](https://github.com/github/spec-kit/issues/5387).
Packaging (standalone repo + release + Preset Submission issue vs bundled
first-party preset under `presets/`) is deferred until the maintainer picks
the vehicle; `preset.repository`/`author` are placeholders.

## Install (local, development)

```bash
specify preset add --dev /path/to/spec-kit/presets/ui-verify
```

Requires Spec Kit >= 1.4.0 (the delta was built on the v1.4.0 core
templates; `replace` strategy pins effective templates to this content).
