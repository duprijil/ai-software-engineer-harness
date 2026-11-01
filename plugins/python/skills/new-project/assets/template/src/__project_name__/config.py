from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class ProjectConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.config", extra="ignore", frozen=True)

    project_name: str
    env_name: str
    postgres_host: str
    postgres_host_port: int
    postgres_db: str
    postgres_user: str


class ProjectSecrets(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.secrets", extra="ignore", frozen=True)

    postgres_password: SecretStr
