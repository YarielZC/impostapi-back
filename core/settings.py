from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    MONGO_URI: str = Field(alias="MONGO_URI")
    DB_NAME: str = Field(alias="DB_NAME")
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
