---
name: architecture
description: Defines the mandatory repository, domain and layer structure for Python projects (DDD, Clean Architecture). Use whenever creating, moving or organizing Python modules or folders, deciding where code belongs, adding code that crosses domains, or reviewing project structure.
---

# Architecture

## Repository layout

```
<repo>/
├── src/<project>/
│   ├── config.py
│   ├── core/
│   └── <domain>/
├── infra/docker/
│   ├── docker-compose.yml
│   └── <service>/
├── docs/
│   ├── specs/
│   └── domains/
├── .github/workflows/quality.yaml
├── .env.config
├── .env.secrets
├── .env.secrets.example
├── .importlinter
├── .python-version
├── AGENTS.md
├── CLAUDE.md
├── Makefile
├── README.md
├── pyproject.toml
├── sonar-project.properties
└── uv.lock
```

Optional root folders: `notebooks/` for exploration, and gitignored `data/` for local data. Production code never lives in either.

## Domain layout

A domain is a bounded context. These are the only folders allowed in it:

```
<domain>/
├── models/        entities with their DTOs, plus exceptions.py
├── use_cases/     one business use case per file
├── adapters/      ABCs and their implementations
├── entrypoints/   how the outside world calls the domain
│   ├── container.py
│   ├── cli/
│   ├── api/
│   └── tui/
└── resources/     non-Python assets only: SQL, prompts, schemas, templates
```

Create a folder only when it has something in it.

## Layers

Dependencies point inward only:

| Layer | May import | Must never |
|---|---|---|
| `entrypoints` | everything in its domain, `config.py` | hold business logic |
| `use_cases` | `adapters/*_abc.py`, `models` | import concrete adapters, config or the DI library |
| `adapters` | `models` | import use cases, config or the DI library |
| `models` | `core.models` | import any other layer, or a database or web library |

Any layer may also import the same or a lower layer of `core`. Entrypoints parse input, get a use case from the container, call `execute()` and format output. Airflow DAGs and Prefect flows are entrypoints too, for example `entrypoints/dags/`.

## Domain types

| Type | May import | Imported by |
|---|---|---|
| `core` | no other domain | all domains |
| Normal domain | `core` | combined domains |
| Combined domain | `core` and normal domains | nothing |

- **`core`** is the shared kernel. It has only `models/` and `adapters/`, and holds no business terms.
- **Combined domains** implement workflows spanning domains. Name them after the business capability, such as `market_analysis`, never `tools` or `orchestration`. They have the same folders as any domain. Their use cases may use other domains' use cases, ABCs and models, and their `container.py` wires the adapters of the domains they combine.
- **Versioned concepts:** a breaking new version of a concept is a new domain, such as `mapping_package_v2` next to `mapping_package_v3`. Never branch with `if version ==`. Conversion between versions belongs in a combined domain.

## Code that doesn't fit

There is no escape hatch. The only Python file outside a domain is `config.py`, and `__init__.py` files stay empty.

1. Business rule for one entity: put it on the model.
2. Business flow: make it a use case.
3. Talks to anything external, or is a technical helper for one domain: make it an adapter.
4. Technical helper used by two or more domains: put it in `core/adapters/`.
5. A distinct business concept: create a new domain with `python:new-domain`.

Never create `utils`, `helpers`, `common`, `shared`, `services`, `tools` or `orchestrator` modules.

## Enforcement

`make check-architecture` enforces these rules with import-linter. See `python:quality-checks`.

## Existing repos

New code follows these rules even when the repo does otherwise. Don't restructure existing code unless the ticket asks for it. Use `python:audit-architecture` to report the gaps.
