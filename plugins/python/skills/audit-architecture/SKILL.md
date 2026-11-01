---
name: audit-architecture
description: Audits an existing Python repository against the harness rules and reports the differences, without changing anything. Use when asked to audit, assess or review a repo's architecture, compliance or conventions, or to plan a migration to the harness structure.
---

# Audit architecture

This skill is read-only. Don't change files, or run anything that does. Skip tests, as they're out of scope.

Never print values from `.env` files. Only look at variable names.

## Checks

Inspect the repo with commands such as `git ls-files` and targeted reads, and record evidence with `file:line`.

**Structure**
- `src/<project>/<domain>/` layout
- Only allowed folders in domains. List every other folder or loose Python file.
- Only `config.py` outside domains, and empty `__init__.py` files

**Naming**
- Adapters are `<what>_<technology>.py` with a `<what>_abc.py` port
- Use cases are verb + noun, with `execute()` classes
- Entrypoints are under channel subfolders
- No banned names

**Dependencies**
- Use cases don't create or import concrete adapters
- Adapters implement ABCs, and don't read config or the environment
- A `container.py` exists in entrypoints
- Domains import only `core`. Cross-domain imports are confined to combined domains.
- `.importlinter` exists and covers all contracts

**Code**
- Count comments and docstrings per package
- Run `make check-types` only if it exists and writes nothing beyond caches. Otherwise, note how complete the type hints look.
- Models inherit from one base with `extra="forbid"`
- Domain exceptions are in `models/exceptions.py`
- No loose `print`, or logging configured outside entrypoints

**Config**
- `.env.config`, `.env.secrets` and `.env.secrets.example` exist, and only `.env.secrets` is ignored
- Secrets aren't tracked by git. Check with `git ls-files`.
- `pydantic-settings` with `SecretStr` is in use

**Infra**
- `infra/docker/` layout
- All compose rules from `python:infrastructure`, particularly floating image tags, hardcoded values, dead config and missing names

**Makefile**
- Exists, and follows `python:makefile`, with all standard targets

**CI and git**
- Follows `python:ci` and `python:git-workflow`
- Recent commits and branch names follow the format. Check with `git log --oneline -20`.

**Docs**
- `AGENTS.md`, `CLAUDE.md`, `docs/domains/` and `docs/specs/` exist
- Docs match the code

## Report

```markdown
# Audit: <repo>

## Summary
<2-3 sentences, and the biggest risks>

## Scorecard
| Area | Status | Findings |
|---|---|---|
| Structure | Fails | 4 |

## Findings
### Structure
- **[High]** `agent/orchestrator.py:1` is outside the allowed folders. Move to `agent/use_cases/`.

## Suggested migration order
1. <Highest value, lowest risk first>
```

Rate each finding:

- **High:** breaks the architecture or exposes a secret
- **Medium:** breaks a rule but is contained
- **Low:** style or naming

Group repeated issues into one finding with a count and examples. Report only what you verified, and note anything you couldn't check. Finish without fixing, and let the engineer choose what to act on.
