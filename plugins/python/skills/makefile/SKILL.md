---
name: makefile
description: Defines the Makefile standard for all projects, including single-responsibility targets, verb-noun naming, icons and colored output. Use whenever adding, changing or running a project command, creating a Makefile, or adding an entrypoint, check or Docker service that needs a target.
---

# Makefile

Every project has one root `Makefile`, and every project command is a target. If you run a useful command twice, it should be a target. The base file is `skills/new-project/assets/template/Makefile`.

## Rules

1. **Single responsibility:** a target does one job. A target that combines others only lists them as prerequisites or calls them.
2. **Verb-noun names**, lowercase, separated by hyphens: `check-lint`, `up-postgres`, `ingest-cars`.
3. **`.PHONY` directly above each target**, rather than in one long list.
4. **No comments or section banners**, as with any other file.
5. **Progress and result output** for targets that do work.
6. **No secrets:** include only `.env.config`, with `-include .env.config`. Never include `.env.secrets`, and never use a bare `export`.
7. **Entrypoint per target:** every runnable entrypoint gets a target.
8. Use variables for repeated paths and commands. Pin tool versions.

## Header

```make
SHELL := /bin/bash -o pipefail
.DEFAULT_GOAL := help

-include .env.config

BUILD_PRINT := \e[1;34m
END_BUILD_PRINT := \e[0m
ICON_DONE := [✔]
ICON_ERROR := [x]
ICON_WARNING := [!]
ICON_PROGRESS := [-]

define print_progress
	@ echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) $(1)$(END_BUILD_PRINT)"
endef

define print_done
	@ echo -e "$(BUILD_PRINT)$(ICON_DONE) $(1)$(END_BUILD_PRINT)"
endef

define print_warning
	@ echo -e "$(BUILD_PRINT)$(ICON_WARNING) $(1)$(END_BUILD_PRINT)"
endef
```

Don't use commas in `$(call ...)` text, because Make treats them as argument separators.

## Target shape

```make
.PHONY: check-lint
check-lint:
	$(call print_progress,Checking lint)
	@ uv run ruff check src
	$(call print_done,Lint check passed)
```

## Standard targets

| Group | Targets |
|---|---|
| Help | `help` |
| Setup | `install-uv`, `check-uv`, `install`, `install-dev`, `setup-env` |
| Format | `format` |
| Checks | `check-format`, `check-lint`, `check-types`, `check-architecture`, `check-complexity`, `check` |
| Stack | `up`, `up-<service>`, `down`, `logs` |
| Run | `run-<entrypoint>`, or a business verb such as `ingest-cars` |

`check` only lists the other checks as prerequisites:

```make
.PHONY: check
check: check-format check-lint check-types check-architecture check-complexity
	$(call print_done,All checks passed)
```

`help` lists target names from the Makefile, so it needs no comments and no upkeep:

```make
.PHONY: help
help:
	@ grep -E '^[a-z][a-z0-9-]*:' Makefile | cut -d: -f1 | sort
```

## Service and entrypoint targets

```make
.PHONY: up-postgres
up-postgres:
	@ $(MAKE) up SERVICE=postgres

.PHONY: ingest-cars
ingest-cars:
	$(call print_progress,Ingesting cars)
	@ uv run python -m my_project.car.entrypoints.cli.ingest_cars
	$(call print_done,Cars ingested)
```

## No test targets

Don't add `test` targets, as testing is the engineer's job. See `python:testing-policy`.
