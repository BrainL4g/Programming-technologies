import os
import secrets

from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = os.path.join(os.path.dirname(__file__), "../../.env")


class Config(BaseSettings):
    DATABASE_PASSWORD: str
    DATABASE_USER: str
    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: int = 5432
    DATABASE_NAME: str = "tp"

    JWT_ALG: str
    JWT_SECRET: str = secrets.token_urlsafe(32)
    JWT_ACCESS_EXP: int
    JWT_REFRESH_EXP: int
    EMAIL_RESET_CODE_EXP: int

    REDIS_HOST: str
    REDIS_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False

    model_config = SettingsConfigDict(env_file=DOTENV)

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        password = self.DATABASE_PASSWORD.replace("@", "%40").replace(":", "%3A")
        url = (
            f"postgresql+asyncpg://{self.DATABASE_USER}:{password}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )
        return PostgresDsn(url)

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


settings = Config()
