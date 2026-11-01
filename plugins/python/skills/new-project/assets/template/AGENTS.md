# {{project_name}}

{{project_description}}

## Commands

- `make install-dev`: install dependencies
- `make setup-env`: create `.env.secrets`
- `make up`, `make down`: start and stop the stack
- `make format`: format and auto-fix
- `make check`: run all quality checks
- `make help`: list every command

## Ticket format

`{{ticket_format}}`. No work starts without a ticket.

## Domains

| Domain | Type | Purpose | Details |
|---|---|---|---|
| core | shared kernel | Base model and shared abstractions | [docs/domains/core.md](docs/domains/core.md) |

## Rules

- Code lives in `src/{{project_name}}/<domain>/`, using only `models/`, `use_cases/`, `adapters/`, `entrypoints/`, plus `resources/` for non-Python assets.
- Layers point inward: entrypoints, use_cases, adapters, models.
- Use cases are `execute()` classes that receive ABCs through the constructor.
- Only `entrypoints/container.py` creates concrete adapters and reads config or secrets.
- Normal domains import only `core`. Combined domains may import others, and nothing imports them.
- Adapter files are named `<what>_<technology>.py`, and each adapter implements `<what>_abc.py`.
- Never write comments or docstrings. Only tool directives such as `# type: ignore` are allowed.
- Type everything. `make check-types` runs mypy strict.
- Never create, edit or run tests. The engineer does the testing. End each task with a short list of what to test.
- Never commit or push unless asked.

## Docs

- Features need an approved spec in `docs/specs/` before any code.
- Each domain's language, responsibilities and invariants live in `docs/domains/<domain>.md`.
- Update this file and the domain doc whenever a command, domain or invariant changes.

## Known pitfalls

None yet. Add project-specific traps here when they cost someone time.
