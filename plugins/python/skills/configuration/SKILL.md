---
name: configuration
description: Defines how Python projects split project config from secrets using .env.config, .env.secrets and pydantic-settings. Use whenever adding or reading an environment variable, setting, port, password, API key, token or connection string, or when touching .env files or config.py.
---

# Configuration

## Files

| File | Holds | Git |
|---|---|---|
| `.env.config` | non-secret values: versions, hosts, ports, names, feature switches | committed |
| `.env.secrets` | passwords, tokens, API keys | gitignored, mode 600 |
| `.env.secrets.example` | the same keys as `.env.secrets`, with empty values | committed |

## Classifying a variable

Ask: would it cause harm if published? If yes, it's a secret. Otherwise, it's config.

- A variable belongs to exactly one file.
- Usernames are config, unless they are themselves sensitive.
- Never store a value that mixes both, such as a URL containing a password. Keep host, port and user in config and the password in secrets, then assemble the URL in compose or in the adapter.
- Never put a real secret in `.env.config`, in code, in compose or in docs, even as an example.

## Python

`src/<project>/config.py` holds both settings classes:

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.config", extra="ignore", frozen=True)

    env_name: str
    postgres_host: str
    postgres_host_port: int


class ProjectSecrets(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.secrets", extra="ignore", frozen=True)

    postgres_password: SecretStr
```

- Secrets are always `SecretStr`. Call `.get_secret_value()` at the last moment, inside the adapter.
- Don't give defaults to values that belong in the env files, so missing values fail at startup.
- Never read `os.environ` directly.

## Who reads it

Only `entrypoints/container.py` reads settings, and passes plain values to adapter constructors. Adapters, use cases and models never import `config.py`. `make check-architecture` enforces this for those three layers, but can't tell `container.py` from other entrypoint files, so CLI and API modules must follow it by convention.

## Tools

- **Compose** loads both files: `docker compose --env-file .env.config --env-file .env.secrets`.
- **Makefile** includes only `.env.config`, and never loads secrets into its environment. See `python:makefile`.
- **CI** gets secrets from the CI secret store. See `python:ci`.

## Adding a variable

1. Classify it.
2. Add it to `.env.config`, or to `.env.secrets` and `.env.secrets.example`.
3. Add a typed field to `ProjectConfig` or `ProjectSecrets`.
4. Wire it in the container.
5. If it's used by a compose service, reference it as `${VAR}`.

## Multiple environments

`ENV_NAME` in `.env.config` names the environment. A deployed environment gets its own values from its deployment process, and a secret manager like Vault generates `.env.secrets` there. Add layered per-environment files only when a real environment requires them.
