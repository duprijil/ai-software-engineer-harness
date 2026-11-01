---
name: design-patterns
description: Lists which design patterns to use in Python projects, where each lives in the domain structure, and how to avoid overengineering. Use when choosing a design, when several implementations or conditional branches appear, or when structuring validation pipelines, retries or tracing.
---

# Design patterns

Patterns are welcome when they solve a problem you have now. Before adding one, name the concrete duplication or branching it removes. If you can't, write the simple version.

## Preferred patterns

| Pattern | Use when | Where |
|---|---|---|
| Repository | Domain objects are persisted | `adapters/repository_abc.py`, `repository_<technology>.py` |
| Adapter | Wrapping any external system | `adapters/<what>_<technology>.py` |
| Strategy | Interchangeable algorithms or providers | an ABC plus one adapter per variant, selected in the container |
| Factory | Building complex objects or clients | container providers, `core/adapters/` for shared clients |
| Chain of Responsibility | Independent validation or processing steps that run in order | `adapters/validator_abc.py` plus one class per step |
| Decorator | Cross-cutting behavior such as retries and tracing | a function in `core/adapters/`, applied at the class or function |
| Template Method | Variants share a fixed algorithm, differing in a few steps | an ABC with concrete and abstract methods |
| Command | A use case: `execute()` with its collaborators | `use_cases/` |

## Replacing conditionals

When an `if` or `match` selects behavior by type, version or provider, and appears in more than one place, replace it with Strategy. Choose the implementation in the container, so use cases never see the choice.

## Generic repository

Use a generic base only when two or more repositories share the same real behavior:

```python
from abc import ABC, abstractmethod

from my_project.core.models.core_model import CoreModel


class RepositoryABC[ModelT: CoreModel](ABC):
    @abstractmethod
    def create(self, model: ModelT) -> str:
        raise NotImplementedError

    @abstractmethod
    def read(self, model_id: str) -> ModelT:
        raise NotImplementedError
```

## Chain of Responsibility

```python
from abc import ABC, abstractmethod

from my_project.package.models.package import Package


class ValidationStepABC(ABC):
    def __init__(self, next_step: "ValidationStepABC | None" = None) -> None:
        self._next_step: ValidationStepABC | None = next_step

    def validate(self, package: Package) -> None:
        self._check(package=package)
        if self._next_step is not None:
            self._next_step.validate(package=package)

    @abstractmethod
    def _check(self, package: Package) -> None:
        raise NotImplementedError
```

Build the chain in the container.

## Tracing as a decorator

Tracing is optional, and only for projects that need it. Keep it in `core/adapters/tracer.py`, off by default, and enabled by a value in `.env.config`. Use a `traced_routine` decorator for functions and `traced_class` for classes. Never record arguments that may contain secrets.

## Avoid

- Singletons written by hand. Use a container `Singleton`.
- Service locators, and passing the container into use cases or adapters.
- Abstract factories, visitors and event buses without a concrete need.
- Inheritance deeper than one abstract base and one concrete class, unless a real hierarchy demands it.
