from pydantic import SecretStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfigs(BaseSettings):
    db_name: str
    user: str
    password: SecretStr
    host: str
    port: int
    url: PostgresDsn | None = None
    dev_env: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf8", extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.url:
            self.url = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=self.db_name,
            ).unicode_string()


class Configs(BaseSettings):
    db_configs: DBConfigs = DBConfigs()


def setup_configs():
    configs = Configs()
    return configs
