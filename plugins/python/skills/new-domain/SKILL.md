---
name: new-domain
description: Adds a new domain (bounded context) to a Python project, including folders, container, domain doc, import-linter contracts and AGENTS.md entry. Use when asked to add a domain, bounded context, module or a new version of a concept, or when code fits no existing domain.
---

# New domain

## 1. Decide the type

| If the domain... | Type |
|---|---|
| owns its own business concept | normal |
| coordinates two or more domains | combined, named after the business capability |
| is a breaking new version of a concept | normal, named `<concept>_v<n>` |

Use a singular noun in snake_case. If the choice isn't clear, ask the engineer.

## 2. Create the folders

Create only the folders the domain needs now, and an empty `__init__.py` in each package:

```
src/<project>/<domain>/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── exceptions.py
├── use_cases/
│   └── __init__.py
├── adapters/
│   └── __init__.py
└── entrypoints/
    ├── __init__.py
    └── container.py
```

Follow `python:naming` and `python:dependency-injection` for the code. A channel like `entrypoints/cli/` is its own package, and needs an `__init__.py`. `exceptions.py` starts with the base error:

```python
class CarError(Exception):
    pass
```

## 3. Update `.importlinter`

Every package listed in a contract must exist, or `lint-imports` fails. Add only entries for folders you created, and add the rest when those folders appear.

**All domains:**

- Add `<project>.<domain>` to `containers` in `layers`.
- Add its `models`, `adapters` and `use_cases` to `source_modules` in `config-access` and `di-stays-in-entrypoints`.
- Add `<project>.<domain>` to `forbidden_modules` in `core-isolated`.
- Add its `use_cases` to `source_modules` in `use-cases-depend-on-abcs`.
- Add each concrete adapter module to `forbidden_modules` in `use-cases-depend-on-abcs`. ABC modules don't go there.

**Normal domains:** add `<project>.<domain>` to `modules` in `domain-independence`, and to `source_modules` in `combined-domains-on-top`, if those contracts exist.

**Combined domains:** add `<project>.<domain>` to `forbidden_modules` in `combined-domains-on-top`. Don't add it to `domain-independence`.

Create a contract the first time it's needed:

```ini
[importlinter:contract:core-isolated]
name = Core imports no other domain
type = forbidden
source_modules =
    <project>.core
forbidden_modules =
    <project>.<first_domain>

[importlinter:contract:use-cases-depend-on-abcs]
name = Use cases never import concrete adapters
type = forbidden
source_modules =
    <project>.<domain>.use_cases
forbidden_modules =
    <project>.<domain>.adapters.<what>_<technology>

[importlinter:contract:domain-independence]
name = Normal domains do not import each other
type = independence
modules =
    <project>.<first_domain>
    <project>.<second_domain>

[importlinter:contract:combined-domains-on-top]
name = Nothing imports a combined domain
type = forbidden
source_modules =
    <project>.core
    <project>.<normal_domain>
forbidden_modules =
    <project>.<combined_domain>
```

`domain-independence` needs at least two normal domains. `combined-domains-on-top` applies once a combined domain exists. `use-cases-depend-on-abcs` applies once a concrete adapter exists.

## 4. Update the docs

- Create `docs/domains/<domain>.md`, following `python:ai-docs`.
- Add a row to the domains table in `AGENTS.md`.

## 5. Add commands

Give each runnable entrypoint a Makefile target, following `python:makefile`.

## 6. Verify

```bash
make format
make check
```
