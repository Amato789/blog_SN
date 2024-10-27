from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: Literal["DEV", "TEST", "PROD"]
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str
    SECRET_KEY: str
    ALGORITHM: str
    OPENAI_API_KEY: str
    OPENAI_PROJECT_NAME: str
    REDIS_HOST: str
    REDIS_PORT: int
    OPENAI_API_KEY_2: str
    OPENAI_PROJECT_NAME_2: str

    @property
    def get_database_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def get_test_database_url(self):
        return (f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@"
                f"{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
