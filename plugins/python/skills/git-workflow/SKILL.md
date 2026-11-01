---
name: git-workflow
description: Defines branch names, simplified Conventional Commits with ticket IDs, the develop and main flow, and pull request rules. Use whenever creating a branch, writing a commit message, opening a pull request, cutting a release or a hotfix, or starting work without a ticket.
---

# Git workflow

## Ticket rule

No work without a ticket. Before changing code, confirm the ticket ID, and if you don't have one, ask for it. Questions and read-only investigation need no ticket.

`AGENTS.md` sets the project's format: `TED-123` for Jira, or `GH-123` for GitHub issues. GitHub auto-links `GH-123`, and it's safe in branch names, which `#123` isn't.

## Agent behavior

- Never commit, push, merge or open a pull request unless asked.
- Never force-push `develop` or `main`, or commit directly to them.

## Branches

`develop` is the default branch. `main` holds released code.

Format: `<type>/<slug>/<ticket>`

```
feature/add-mongodb-repository/TED-123
fix/handle-empty-response/TED-124
hotfix/fix-login-crash/TED-125
refactor/extract-minio-client/TED-126
docs/describe-car-domain/TED-127
chore/bump-uv/TED-128
```

The slug is a few lowercase words, separated by hyphens, in the imperative.

## Commits

Format: `type(ticket): summary`

```
feat(TED-123): add mongodb repository
fix(TED-124): handle empty provider response
refactor(TED-126): extract minio client
docs(TED-127): describe car domain
chore(TED-128): bump uv
```

| Type | Use for |
|---|---|
| `feat` | new behavior |
| `fix` | a bug fix |
| `refactor` | structure change with the same behavior |
| `docs` | documentation only |
| `chore` | tooling, dependencies, CI, infra |

The summary is imperative, lowercase, under about 72 characters, with no period. A body is optional. Don't add other types.

## Flow

```
feature/x/TED-1 ──PR squash──▶ develop
fix/y/TED-2     ──PR squash──▶ develop

develop ──PR merge commit──▶ main ──▶ tag v1.2.0

hotfix/z/TED-3 ──PR squash──▶ main ──▶ tag v1.2.1
main ──PR merge commit──▶ develop
```

- **Normal work:** branch from `develop`, then squash-merge a PR back. One ticket gives one commit on `develop`.
- **Release:** PR from `develop` to `main`, merged with a merge commit, then tag `vX.Y.Z` on `main`.
- **Hotfix:** branch from `main`, squash-merge to `main`, tag, then open a PR from `main` to `develop`.

Release and back-merge PRs need no ticket, and are titled `release: v1.2.0` and `chore: merge main into develop`.

## Pull requests

- The title uses the commit format, because it becomes the squash commit.
- The body has the ticket link, a short summary, a link to the spec if there is one, and the "What to test" list from `python:testing-policy`.
- `make check` and Sonar must pass. See `python:ci`.
- The engineer reviews and merges.
