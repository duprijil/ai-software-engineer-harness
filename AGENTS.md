# Software Engineer Harness

A Claude Code plugin marketplace that encodes one engineer's practices. Each language is a plugin in `plugins/`.

## Commands

- `claude plugin validate .`: validate the marketplace
- `claude plugin validate plugins/python`: validate the Python plugin

## Layout

- `.claude-plugin/marketplace.json`: lists the plugins
- `plugins/python/hooks/core_rules.md`: always-on rules summary
- `plugins/python/skills/<skill>/SKILL.md`: one skill per topic
- `plugins/python/skills/new-project/assets/template/`: the generated project

## Rules for changing the harness

- A rule lives in exactly one skill. Others link to it as `python:<skill>`.
- Only rules that must hold when no skill has loaded go in `core_rules.md`. Keep that file short, as it costs context in every session.
- Keep `core_rules.md` and the template's `AGENTS.md` consistent with the skills.
- A skill's `description` decides when it loads, so state what it covers and when to use it.
- Harness files follow their own rules: no comments, including in templates and code examples.
- Never add real project data or secrets to templates.
- Bump `version` in `plugins/python/.claude-plugin/plugin.json` on each change, or installed copies won't update.

## Verifying template changes

Generate a throwaway project outside this repo from `new-project/assets/template`, add at least two normal domains and one combined domain following `new-domain`, then run `make check`. Also break a contract on purpose, and confirm the check fails. Keep tool versions the same across `pyproject.toml`, the `Makefile` and `quality.yaml`.
