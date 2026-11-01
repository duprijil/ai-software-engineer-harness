# core

Shared kernel. Holds what every domain needs and knows nothing about any of them.

## Responsibilities

- `CoreModel`: the base class for all Pydantic models
- Abstractions and technical helpers shared by two or more domains

## Language

None. Business terms belong in their own domain.

## Invariants

- `core` never imports another domain.
- `core` has no `use_cases` or `entrypoints`.
