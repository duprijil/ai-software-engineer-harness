SHELL := /bin/bash -o pipefail
.DEFAULT_GOAL := help

-include .env.config

BUILD_PRINT := \e[1;34m
END_BUILD_PRINT := \e[0m
ICON_DONE := [✔]
ICON_ERROR := [x]
ICON_WARNING := [!]
ICON_PROGRESS := [-]

UV_VERSION := 0.13.6
SRC_PATH := src/{{project_name}}
COMPOSE := docker compose --env-file .env.config --env-file .env.secrets -f infra/docker/docker-compose.yml

define print_progress
	@ echo -e "$(BUILD_PRINT)$(ICON_PROGRESS) $(1)$(END_BUILD_PRINT)"
endef

define print_done
	@ echo -e "$(BUILD_PRINT)$(ICON_DONE) $(1)$(END_BUILD_PRINT)"
endef

define print_warning
	@ echo -e "$(BUILD_PRINT)$(ICON_WARNING) $(1)$(END_BUILD_PRINT)"
endef

.PHONY: help
help:
	@ grep -E '^[a-z][a-z0-9-]*:' Makefile | cut -d: -f1 | sort

.PHONY: install-uv
install-uv:
	$(call print_progress,Installing uv $(UV_VERSION))
	@ curl -LsSf https://astral.sh/uv/$(UV_VERSION)/install.sh | sh
	$(call print_done,uv $(UV_VERSION) installed)

.PHONY: check-uv
check-uv:
	@ command -v uv >/dev/null 2>&1 || $(MAKE) install-uv

.PHONY: install
install: check-uv
	$(call print_progress,Installing project dependencies)
	@ uv sync --no-dev
	$(call print_done,Project dependencies installed)

.PHONY: install-dev
install-dev: check-uv
	$(call print_progress,Installing project and dev dependencies)
	@ uv sync
	$(call print_done,Project and dev dependencies installed)

.PHONY: setup-env
setup-env:
	$(call print_progress,Creating .env.secrets from the example)
	@ cp -n .env.secrets.example .env.secrets || true
	@ chmod 600 .env.secrets
	$(call print_warning,Fill the empty values in .env.secrets)

.PHONY: format
format:
	$(call print_progress,Formatting code)
	@ uv run ruff format src
	@ uv run ruff check --fix src
	$(call print_done,Code formatted)

.PHONY: check-format
check-format:
	$(call print_progress,Checking format)
	@ uv run ruff format --check src
	$(call print_done,Format check passed)

.PHONY: check-lint
check-lint:
	$(call print_progress,Checking lint)
	@ uv run ruff check src
	$(call print_done,Lint check passed)

.PHONY: check-types
check-types:
	$(call print_progress,Checking types)
	@ uv run mypy
	$(call print_done,Type check passed)

.PHONY: check-architecture
check-architecture:
	$(call print_progress,Checking architecture)
	@ uv run lint-imports
	$(call print_done,Architecture check passed)

.PHONY: check-complexity
check-complexity:
	$(call print_progress,Checking complexity)
	@ uv run xenon $(SRC_PATH) --max-absolute C --max-modules C --max-average A
	$(call print_done,Complexity check passed)

.PHONY: check
check: check-format check-lint check-types check-architecture check-complexity
	$(call print_done,All checks passed)

.PHONY: up
up:
	$(call print_progress,Starting $(if $(SERVICE),$(SERVICE),all services) for $(ENV_NAME))
	@ $(COMPOSE) up -d --build $(SERVICE)
	$(call print_done,Started $(if $(SERVICE),$(SERVICE),all services))

.PHONY: up-postgres
up-postgres:
	@ $(MAKE) up SERVICE=postgres

.PHONY: down
down:
	$(call print_progress,Stopping services for $(ENV_NAME))
	@ $(COMPOSE) down
	$(call print_done,Services stopped)

.PHONY: logs
logs:
	@ $(COMPOSE) logs -f $(SERVICE)
