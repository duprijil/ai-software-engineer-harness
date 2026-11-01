---
name: infrastructure
description: Defines the strict infra folder layout and docker-compose standard for Python projects. Use whenever adding or changing a Docker service, Dockerfile, compose file, volume, network or anything under infra/.
---

# Infrastructure

## Layout

```
infra/
└── docker/
    ├── docker-compose.yml
    ├── docker-compose.<env>.yml
    ├── postgres/
    │   └── init/
    └── <service>/
        ├── Dockerfile
        └── <service config>
```

- Everything a service needs lives in `infra/docker/<service>/`.
- There is one `docker-compose.yml`. Add a `docker-compose.<env>.yml` override only when a real environment needs one.

## Compose rules

1. **One stack:** a top-level `name: ${PROJECT_NAME}_${ENV_NAME}` groups all services.
2. **Every service has a name:** `container_name: ${PROJECT_NAME}_${ENV_NAME}_<service>`.
3. **Pinned images via variables:** `image: postgres:${POSTGRES_VERSION}`. Never `latest` or a floating tag such as `3-latest`. Versions live in `.env.config`.
4. **No hardcoded values:** versions, ports, credentials, database names and bucket names all come from `${VAR}`. Container paths defined by the image, like `/var/lib/postgresql/data`, may stay literal.
5. **Named volumes for state:** every stateful service uses a named volume, and its data never lives in a bind mount. Stateless services need no volume. Read-only inputs, like init scripts, may be bind mounts.
6. **Named resources:** volumes and networks get explicit names based on `${PROJECT_NAME}_${ENV_NAME}`.
7. **One project network** that every service joins.
8. **No dead config:** no comments, commented-out services, or unused volumes or networks. Git keeps the history.
9. No top-level `version:` key, as Compose no longer uses it.
10. No environment variables with hardcoded secrets. Secrets come from `.env.secrets`.

## Standard service

```yaml
name: ${PROJECT_NAME}_${ENV_NAME}

services:
  postgres:
    image: postgres:${POSTGRES_VERSION}
    container_name: ${PROJECT_NAME}_${ENV_NAME}_postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGPORT: ${POSTGRES_CONTAINER_PORT}
    ports:
      - "${POSTGRES_HOST_PORT}:${POSTGRES_CONTAINER_PORT}"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres/init:/docker-entrypoint-initdb.d
    networks:
      - project_network

volumes:
  postgres_data:
    name: ${PROJECT_NAME}_${ENV_NAME}_postgres_data

networks:
  project_network:
    name: ${PROJECT_NAME}_${ENV_NAME}_network
    driver: bridge
```

## Adding a service

1. Add the service to `docker-compose.yml` following the rules above.
2. Add its version, ports and names to `.env.config`, and any credentials to `.env.secrets` and `.env.secrets.example`.
3. Put its Dockerfile and config in `infra/docker/<service>/`.
4. Add an `up-<service>` target to the Makefile.
5. Verify the file resolves:

```bash
docker compose --env-file .env.config --env-file .env.secrets -f infra/docker/docker-compose.yml config
```

Run compose only through `make up`, `make down` and `make logs`.
