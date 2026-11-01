---
name: ai-docs
description: Defines AI-driven documentation for Python projects, including AGENTS.md, CLAUDE.md, docs/specs and docs/domains. Use whenever writing or updating project documentation, changing commands or domains, or recording knowledge that would otherwise become a code comment.
---

# AI-driven docs

Docs are written for agents first. Code holds no comments or docstrings, so knowledge lives in a small set of files that an agent can load only when it needs them.

| File | Purpose | Loaded |
|---|---|---|
| `AGENTS.md` | short project map | every session |
| `CLAUDE.md` | one line: `@AGENTS.md` | every session |
| `docs/domains/<domain>.md` | what a bounded context means | when working in that domain |
| `docs/specs/<ticket>-<domain>-<slug>.md` | what one feature must do | when working on that feature |
| `README.md` | short human setup | by people |

Don't add other doc types. Don't use doc generators like Antora, or duplicate what code, `make help` or `git log` already show.

## Writing rules

- **Short and factual.** Every line must change what an agent would do.
- **Specific:** real commands, paths and names.
- **Current:** update docs in the same change as the behavior they describe. A stale doc is worse than none.
- **Link, don't copy.** Facts live in one place.

## AGENTS.md

Keep it under about 100 lines. Sections: purpose, commands, ticket format, domains table, rules, docs, known pitfalls. Add a pitfall only when it has actually cost someone time, such as "ROUND needs a `::numeric` cast on Postgres".

## Domain docs

One file per domain, under about 60 lines:

```markdown
# car

One sentence on what this bounded context is for.

## Responsibilities

What it owns, and what it deliberately doesn't.

## Language

| Term | Meaning |
|---|---|
| Listing | One published ad for a car at a point in time |

## Ports

- `RepositoryABC`: stores cars. Implementations: `RepositoryPostgres`.

## Invariants

- A car's price is always in EUR.
```

Knowledge you'd be tempted to put in a comment goes here if it's about the domain, or in the spec if it's about one feature.

## Specs

Use `python:new-spec`. A new feature needs an approved spec before any code. Bug fixes, refactors and small changes need only a ticket.

The status line moves `Draft` → `Approved` → `Implemented`. When implementation is finished, set `Implemented`, and update the spec if the design changed along the way. Specs are the record of why a feature exists, so don't delete them.
