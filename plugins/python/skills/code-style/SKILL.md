---
name: code-style
description: Defines mandatory Python code style, including no comments, no docstrings, strict typing, Clean Code, DDD modeling, Pydantic models, exceptions and logging. Use whenever writing, editing or reviewing any Python code.
---

# Code style

## No comments, no docstrings

- Never write comments or docstrings, in any file type: Python, YAML, Makefile, Dockerfile, SQL, TOML, shell.
- This holds even when the surrounding code has them.
- Only tool directives may stay: `# type: ignore[code]`, `# noqa: CODE`, shebangs. Always include the specific code.
- Never leave commented-out code.
- When you edit a function or class, remove its comments and docstrings. Leave the rest of the file alone, to keep diffs focused.

If code seems to need an explanation, rename or extract until it doesn't. Domain knowledge goes in `docs/domains/<domain>.md`, and feature reasoning goes in the spec.

Strings used at runtime aren't comments. `Field(description=...)` and Typer `help=...` are allowed.

## Strict typing

Python may be duck-typed, but our code isn't. `make check-types` runs mypy strict.

- Annotate every parameter, return value (including `-> None`), attribute and module-level variable.
- Annotate locals whose type isn't obvious from the right-hand side.
- Use modern syntax, Python 3.12+: `list[str]`, `dict[str, int]`, `X | None`. Never `List` or `Optional`.
- Avoid `Any`. Use a Pydantic model, `TypedDict` or generic. Use `Any` only for truly untyped third-party boundaries, and convert immediately.
- Never return loose `dict` or `tuple` values from a public method. Return a model.

## Clean Code

- A function does one thing. Extract when you need a second level of abstraction.
- Use early returns instead of deep nesting.
- Validate input at the start of `execute()`, and fail with a specific error.
- Use keyword arguments at call sites when there's more than one parameter.
- Mark concrete adapters and use cases `@final`.
- No magic values. Name them, or move them to `.env.config` if they vary by environment.
- No boolean parameters that switch behavior. Make two methods or two strategies.
- No global mutable state.
- All imports are absolute and at the top of the file.

## DDD

- Use the domain's language from `docs/domains/<domain>.md` in names.
- A rule concerning one entity belongs on that entity, as a method or Pydantic validator. Don't keep models as bare data if they have rules.
- Value objects use `frozen=True`.
- Domain models never depend on technology. Mapping to a database or API shape happens in the adapter.

## Models

- Every Pydantic model inherits from `CoreModel` in `core/models/core_model.py`, directly or indirectly.
- One entity per file, with its DTOs in the same file.
- DTOs carry data across a boundary, and always end in `DTO`.

## Exceptions

- Each domain has `models/exceptions.py`, with one base `<Domain>Error` and specific subclasses.
- Adapters translate driver errors into domain errors, using `raise ... from error`.
- Never catch bare `Exception`, except at the outermost entrypoint, where you log it and exit non-zero.
- Never swallow an error silently.

## Logging

- Every module that logs uses `logger: logging.Logger = logging.getLogger(__name__)`.
- Configure logging once at startup, in the entrypoint. Never in `config.py`, adapters or use cases.
- Use lazy formatting: `logger.info("Saved %s", car_id)`.
- Never use `print`. CLIs use `typer.echo` for user output.
- Never log secrets.
- Tracing is off by default. Add OpenTelemetry only when a project needs it. See `python:design-patterns`.
