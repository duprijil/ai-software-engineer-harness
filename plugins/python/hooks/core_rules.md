# Python harness: rules for this session

These rules apply to all code you write, even where the existing project does otherwise. Load the matching `python:*` skill for details.

- **Tickets:** no code change without a ticket ID. If you have none, ask for it.
- **Features:** a feature needs an approved spec in `docs/specs/` before code. Use `python:new-spec`.
- **Structure:** `src/<project>/<domain>/` with only `models/`, `use_cases/`, `adapters/`, `entrypoints/`, plus `resources/` for non-Python assets. Code that fits none of these gets reshaped or becomes a new domain. Never create `utils`, `helpers` or `common`.
- **Domains:** normal domains import only `core`. Combined domains may import others, and nothing imports them. A breaking new version of a concept is a new domain.
- **Dependencies:** layers point inward: entrypoints, use_cases, adapters, models. Use cases are `execute()` classes that receive ABCs through the constructor. Only `entrypoints/container.py` creates concrete adapters and reads config or secrets.
- **Naming:** adapter files are `<what>_<technology>.py`, and each implements `<what>_abc.py`.
- **Comments:** never write comments or docstrings, in any file type. Only tool directives such as `# type: ignore[code]` are allowed. Remove existing ones from code you edit, and leave the rest of the file alone.
- **Types:** type everything. No untyped function, attribute or container provider.
- **Config:** non-secrets go in committed `.env.config`, secrets in gitignored `.env.secrets`.
- **Commands:** every command is a Makefile target. Run `make format`, then `make check`, before finishing.
- **Tests:** never create, edit or run tests. The engineer does the testing. End each task with a short list of what to test.
- **Git:** never commit or push unless asked. Branches are `<type>/<slug>/<ticket>`, and commits are `type(ticket): summary`.
