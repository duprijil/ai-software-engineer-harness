---
name: naming
description: Defines naming rules for Python files, classes, variables and domains. Use whenever creating or renaming a Python file, class, function, adapter, use case, entrypoint, DTO or exception, or when reviewing names.
---

# Naming

## Files and classes

| Kind | File | Class |
|---|---|---|
| Domain folder | `car/`, `mapping_package_v3/`: singular noun | |
| Entity and its DTOs | `models/car.py` | `Car`, `CarCreateDTO`, `CarSummaryDTO` |
| Exceptions | `models/exceptions.py` | `CarError`, `CarNotFoundError` |
| Use case | `use_cases/register_car.py`: verb + noun | `RegisterCar` with `execute()` |
| Port | `adapters/repository_abc.py` | `RepositoryABC` |
| Adapter | `adapters/repository_mongodb.py` | `RepositoryMongoDB` |
| Container | `entrypoints/container.py` | `CarContainer` |
| CLI | `entrypoints/cli/register_car.py` | |
| API | `entrypoints/api/cars.py` | |
| TUI | `entrypoints/tui/car_browser.py` | |

## Adapter files

The pattern is `<what you implement>_<what you adapt to>.py`:

```
adapters/
├── repository_abc.py
├── repository_mongodb.py
├── repository_postgres.py
├── storage_abc.py
├── storage_minio.py
├── provider_abc.py
├── provider_999.py
└── llm_client_openrouter.py
```

The domain folder already names the entity, so don't repeat it. When one domain has two ports of the same kind, add the entity after `<what>`:

```
repository_car_abc.py
repository_car_mongodb.py
repository_listing_abc.py
repository_listing_mongodb.py
```

Don't prefix files with the domain or version. Inside `mapping_package_v3/adapters/`, write `loader_folder.py`, not `mp_v3_loader_folder.py`.

## Variables and parameters

- Use full, descriptive names: `car_repository`, not `repo`. `mapping_package_folder_path`, not `path`.
- Name parameters after their role, not their type: `car_provider`, not `provider_abc`.
- Prefix private attributes with one underscore: `self._car_repository`.
- Exceptions always end in `Error`, never `Exception`.
- Booleans read as a statement: `is_active`, `has_expired`.

## Banned names

Never use these alone or as a suffix for modules, classes or functions:

`manager`, `helper`, `util`, `utils`, `utility`, `common`, `misc`, `base`, `generic`, `shared`, `process`, `handle`, `do_stuff`

Never use these as variable names:

`data`, `info`, `obj`, `item`, `thing`, `stuff`, `value`, `result`, `output`, `input`, `flag`, `temp`, `tmp`, `aux`, `foo`, `bar`, `baz`

Ruff can't check this list, so apply it yourself. Two exceptions: names required by a framework, and a narrow loop or comprehension variable where the type is obvious, such as `car` or `job`.

## Makefile targets and branches

See `python:makefile` and `python:git-workflow`.
