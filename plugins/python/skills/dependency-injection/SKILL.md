---
name: dependency-injection
description: Defines how Python dependencies are abstracted and wired, using ABC ports, constructor injection, execute() use cases and dependency-injector containers in entrypoints. Use whenever writing a use case, adapter, ABC, container or entrypoint, or when one class needs another.
---

# Dependency injection

## Rules

1. A use case is a class with `execute()`, and receives dependencies through its constructor.
2. Use cases depend on ABCs. Every adapter a use case depends on implements an ABC, even with one implementation.
3. Only `entrypoints/container.py` creates concrete adapters and reads config or secrets.
4. Adapters receive plain values through their constructor. They never read the environment or import `config.py`.
5. Only entrypoints import `dependency_injector`. Don't use `@inject`, `Provide[...]` or `container.wire()`.

A class that only serves one adapter internally needs no ABC.

## Port

```python
from abc import ABC, abstractmethod

from my_project.car.models.car import Car


class RepositoryABC(ABC):
    @abstractmethod
    def save(self, car: Car) -> str:
        raise NotImplementedError
```

Keep ports small and shaped by what use cases need, not by the technology. Port signatures use domain models, never `DataFrame`, ORM rows or driver types, unless that type is the domain concept.

## Adapter

```python
from typing import final

from pymongo import MongoClient
from pymongo.collection import Collection

from my_project.car.adapters.repository_abc import RepositoryABC
from my_project.car.models.car import Car


@final
class RepositoryMongoDB(RepositoryABC):
    def __init__(self, mongo_client: MongoClient[dict[str, str]], database_name: str) -> None:
        self._collection: Collection[dict[str, str]] = mongo_client[database_name]["cars"]

    def save(self, car: Car) -> str:
        self._collection.insert_one(car.model_dump(mode="json"))
        return car.car_id
```

ORM classes and query details stay inside the adapter file.

## Use case

```python
from typing import final

from my_project.car.adapters.provider_abc import ProviderABC
from my_project.car.adapters.repository_abc import RepositoryABC
from my_project.car.models.car import Car


@final
class IngestCars:
    def __init__(self, car_provider: ProviderABC, car_repository: RepositoryABC) -> None:
        self._car_provider: ProviderABC = car_provider
        self._car_repository: RepositoryABC = car_repository

    def execute(self) -> int:
        cars: list[Car] = self._car_provider.get()
        for car in cars:
            self._car_repository.save(car=car)
        return len(cars)
```

Pass per-call input to `execute()`, and collaborators to the constructor.

## Container

Each domain has one container, at `entrypoints/container.py`:

```python
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton

from my_project.car.adapters.provider_999 import Provider999
from my_project.car.adapters.repository_postgres import RepositoryPostgres
from my_project.car.use_cases.ingest_cars import IngestCars
from my_project.config import ProjectConfig, ProjectSecrets


class CarContainer(DeclarativeContainer):
    config: Singleton[ProjectConfig] = Singleton(ProjectConfig)
    secrets: Singleton[ProjectSecrets] = Singleton(ProjectSecrets)
    car_provider: Singleton[Provider999] = Singleton(Provider999)
    car_repository: Singleton[RepositoryPostgres] = Singleton(
        RepositoryPostgres,
        host=config.provided.postgres_host,
        port=config.provided.postgres_host_port,
        database_name=config.provided.postgres_db,
        user=config.provided.postgres_user,
        password=secrets.provided.postgres_password,
    )
    ingest_cars: Factory[IngestCars] = Factory(IngestCars, car_provider=car_provider, car_repository=car_repository)
```

- `Singleton` for adapters and clients. `Factory` for use cases.
- Annotate every provider, so mypy strict knows what the container returns.
- Build shared clients with a factory in `core/adapters/`, and wire it in each container that needs it.
- Combined domains use their own container to wire the adapters they need from other domains.

## Entrypoint

```python
import logging

import typer

from my_project.car.entrypoints.container import CarContainer

logger: logging.Logger = logging.getLogger(__name__)
car_cli: typer.Typer = typer.Typer()


@car_cli.command()
def ingest_cars() -> None:
    logging.basicConfig(level=logging.INFO)
    ingested_count: int = CarContainer().ingest_cars().execute()
    logger.info("Ingested %s cars", ingested_count)


if __name__ == "__main__":
    car_cli()
```

## Avoid overengineering

- Don't add generic base classes before two concrete cases share real behavior.
- Don't add ports for pure functions or standard library calls that need no replacing.
- Don't add an interface for use cases.
- Don't create nested or global containers.
