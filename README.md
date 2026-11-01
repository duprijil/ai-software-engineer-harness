# Software Engineer Harness

An AI harness that teaches coding agents how I build software. It's a Claude Code plugin marketplace with one plugin per language. Python is the first.

## Install

From GitHub:

```text
/plugin marketplace add duprijil/ai-software-engineer-harness
/plugin install python@software-engineer-harness
```

From a local clone:

```text
/plugin marketplace add /path/to/ai-software-engineer-harness
/plugin install python@software-engineer-harness
```

Restart Claude Code afterwards. Skills then appear as `/python:<skill>`.

The install command uses the marketplace name, `software-engineer-harness`, from [marketplace.json](.claude-plugin/marketplace.json), so it differs from the repository name.

To pick up new versions:

```text
/plugin marketplace update software-engineer-harness
/plugin update python@software-engineer-harness
```

## What the Python plugin does

Its rules activate in two ways:

- **Always on:** when a session starts in a folder with a `pyproject.toml`, a hook adds a short summary of the core rules.
- **On demand:** Claude loads the matching skill when it's relevant, or you call one directly.

### Standards

| Skill | Covers |
|---|---|
| `architecture` | Repo layout, domains, layers, combined domains |
| `naming` | Files, classes, variables, banned names |
| `dependency-injection` | ABC ports, `execute()` use cases, containers |
| `code-style` | No comments or docstrings, strict typing, Clean Code, DDD |
| `design-patterns` | Which patterns to use and where, without overengineering |
| `configuration` | `.env.config` and `.env.secrets`, pydantic-settings |
| `infrastructure` | `infra/docker` and strict compose rules |
| `makefile` | Makefile standard |
| `quality-checks` | Ruff, mypy strict, import-linter, xenon |
| `testing-policy` | Agents don't test, and hand off a test list |
| `ai-docs` | `AGENTS.md`, domain docs, specs |
| `git-workflow` | Tickets, branches, commits, develop and main flow |
| `ci` | GitHub Actions and SonarCloud |

### Workflows

| Command | Does |
|---|---|
| `/python:new-project` | Scaffolds a complete repo |
| `/python:new-domain` | Adds a domain and its contracts |
| `/python:new-spec` | Interviews you and writes a spec |
| `/python:audit-architecture` | Reports how a repo differs from the rules, read-only |

## Repository layout

```
.claude-plugin/marketplace.json
plugins/
└── python/
    ├── .claude-plugin/plugin.json
    ├── hooks/
    └── skills/
```

To add a language, create `plugins/<language>/` and list it in `marketplace.json`. To change a Python rule, see [AGENTS.md](AGENTS.md).

## License

See [LICENSE](LICENSE).
