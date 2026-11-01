---
name: quality-checks
description: Defines the Python quality tools and thresholds (Ruff, mypy strict, import-linter, xenon) and how to fix failures. Use when running or configuring make check, editing .importlinter or tool settings in pyproject.toml, or when a lint, type, architecture or complexity check fails.
---

# Quality checks

Before finishing any code change, run `make format` and then `make check`.

| Target | Tool | Enforces |
|---|---|---|
| `check-format` | Ruff | formatting, 120-character lines |
| `check-lint` | Ruff | errors, imports, naming, modern syntax, annotations, no `print` |
| `check-types` | mypy strict | full static typing |
| `check-architecture` | import-linter | layers and domain boundaries |
| `check-complexity` | xenon | absolute C, modules C, average A |

## Fixing failures

Fix the code, never the check. Don't lower thresholds, add ignores or edit contracts just to pass.

- **Complexity:** split the function, or replace branching with early returns or Strategy.
- **Architecture:** move the code to the right layer, or depend on an ABC instead. Never add `ignore_imports`.
- **Types:** add the precise type. `# type: ignore[code]` is the last resort, for wrong third-party stubs only. Say so in your final message.

If a check seems genuinely wrong, stop and tell the engineer.

## import-linter contracts

`.importlinter` has one section per rule:

| Contract | Rule |
|---|---|
| `layers` | entrypoints > use_cases > adapters > models, in every domain |
| `config-access` | models, adapters and use cases never import `<project>.config` |
| `di-stays-in-entrypoints` | models, adapters and use cases never import `dependency_injector` |
| `core-isolated` | `core` imports no domain |
| `domain-independence` | normal domains don't import each other |
| `combined-domains-on-top` | nothing imports a combined domain |
| `use-cases-depend-on-abcs` | use cases never import concrete adapters |

`python:new-domain` shows how to extend these.

## Known limits

- **`use-cases-depend-on-abcs` lists concrete adapters explicitly**, since import-linter can't express "everything except `*_abc`". Add each new adapter module to it.
- **`config-access` and DI checks stop at layers.** They can't tell `container.py` from other entrypoint files.
- **Banned names and the no-comments rule aren't automated.** Apply them yourself.

## Tool configuration

Ruff and mypy are configured in `pyproject.toml`. Ruff selects `E, F, W, I, N, UP, B, C4, SIM, RET, ANN, ARG, PTH, T20`. Ruff's `D` docstring rules stay off, because we don't write docstrings.
