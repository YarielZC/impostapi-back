from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    MONGO_URI: str = Field(alias="MONGO_URI")
    DB_NAME: str = Field(alias="DB_NAME")
    TOKEN_DURATION: int = Field(alias="TOKEN_DURATION")
    SECRET_TOKEN_KEY: str = Field(alias="SECRET_TOKEN_KEY")
    ALGORITHM_CRYPT: str = Field(alias="ALGORITHM_CRYPT")
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
