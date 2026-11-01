---
name: new-project
description: Scaffolds a complete new Python repository following the harness, with src layout, infra, Makefile, env files, quality tools, CI, Sonar and AI docs. Use when asked to create, start, bootstrap or scaffold a new Python project or repo.
---

# New project

## 1. Gather inputs

Ask for anything not already given:

| Input | Example |
|---|---|
| `project_name`, in snake_case | `market_radar` |
| `project_description`, one sentence | `Tracks car prices across marketplaces` |
| `ticket_format` | `GH-<number>` or `TED-<number>` |
| `sonar_organization` | `acme` |
| First domain | `car` |
| Docker services needed | `postgres` |

If the target folder isn't empty, stop and ask first.

## 2. Copy the template

The template is in this skill's `assets/template/` folder. Copy it, including hidden files:

```bash
cp -r <skill-dir>/assets/template/. <target>/
mv <target>/src/__project_name__ <target>/src/<project_name>
```

## 3. Replace placeholders

Replace these four tokens in all copied files: `{{project_name}}`, `{{project_description}}`, `{{ticket_format}}`, `{{sonar_organization}}`.

Don't touch `${{ secrets.SONAR_TOKEN }}` in the workflow, as that's GitHub syntax.

## 4. Adjust services

The template includes `postgres` as the reference service. For each needed service, follow `python:infrastructure`. If a service isn't needed, remove it from all of these:

- `infra/docker/docker-compose.yml` and `infra/docker/<service>/`
- `.env.config` and `.env.secrets.example`
- `src/<project_name>/config.py`
- the Makefile's `up-<service>` target

If no services are needed, remove `infra/`, `.env.secrets.example`, and the `up`, `up-*`, `down` and `logs` targets, the `COMPOSE` variable and `setup-env`. Also remove `ProjectSecrets`.

## 5. Install and initialize

```bash
git init -b develop
make install-dev
make setup-env
```

Don't create a commit unless asked.

## 6. Create the first domain

Follow `python:new-domain` for the first domain.

## 7. Verify

```bash
make format
make check
docker compose --env-file .env.config --env-file .env.secrets -f infra/docker/docker-compose.yml config
```

Fix any failure before finishing. Skip the compose command if the project has no services.

## 8. Hand off

Tell the engineer:

- what was created and whether checks passed
- to fill in `.env.secrets`
- the manual CI and Sonar steps from `python:ci`
