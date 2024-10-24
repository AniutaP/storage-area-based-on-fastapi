from dataclasses import dataclass
import os
from dotenv import load_dotenv


load_dotenv()

DATABASE_NAME = os.getenv('DATABASE_NAME')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')


@dataclass
class DatabaseConfig:
    host: str
    port: str
    user: str
    password: str
    database: str

    @property
    def url_create(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


@dataclass
class Config:
    database: DatabaseConfig | None = None


def setup_config():
    config = Config(
        database=DatabaseConfig(
            host=DATABASE_HOST,
            port=DATABASE_PORT,
            user=DATABASE_USER,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME
        ),
    )
    return config

config = setup_config()