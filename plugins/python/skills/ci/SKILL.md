---
name: ci
description: Defines the GitHub Actions pipeline and SonarCloud setup for Python projects, including the coverage-free quality gate. Use whenever creating or changing CI workflows, sonar-project.properties, the Sonar quality gate, or investigating a CI failure.
---

# CI

CI has one workflow, `.github/workflows/quality.yaml`, with two jobs. The base files are in `skills/new-project/assets/template/`.

| Job | Does |
|---|---|
| `check` | `make install-dev`, then `make check` |
| `sonar` | SonarCloud scan, and waits for the quality gate |

It runs on pushes to `develop` and `main`, and on PRs targeting them.

## Rules

- **CI calls Make targets.** Never put check logic in the workflow, so local runs and CI always match.
- **Pin versions:** use a tag the action actually publishes, as not all publish a major tag like `v10`. The uv version must match `UV_VERSION` in the Makefile.
- **Least privilege:** `permissions: contents: read` by default.
- **No test or coverage jobs.** See `python:testing-policy`.
- **Secrets come from GitHub secrets only.** CI doesn't need `.env.secrets` to run checks.
- No comments in workflow files.

## Sonar

`sonar-project.properties` sets the project key, organization, sources and `sonar.qualitygate.wait=true`. It sets no test or coverage properties.

Sonar's default gate requires coverage on new code, so with no tests it would fail every PR. Each project must use a custom gate, which you set up once in the SonarCloud UI:

| Metric, on new code | Condition |
|---|---|
| Reliability rating | A |
| Security rating | A |
| Maintainability rating | A |
| Security hotspots reviewed | 100% |
| Duplicated lines | at most 3% |

Don't add a coverage condition. If a Sonar rule asks for docstrings or comments, disable it in the project's quality profile, as it conflicts with `python:code-style`.

## Manual setup per project

The agent can't do these steps. List them for the engineer when creating CI:

1. Create the SonarCloud project and disable Automatic Analysis.
2. Create and assign the custom quality gate. Custom gates may need a paid plan for private projects.
3. Add a `SONAR_TOKEN` repository secret on GitHub.
4. Set `develop` as the default branch on GitHub.
5. Protect `develop` and `main`: require PRs, and require the `Make check` and `SonarCloud` checks.
6. Allow both squash and merge commits, because the flow uses both.
