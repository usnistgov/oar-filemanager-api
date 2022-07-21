import os
from pydantic import BaseSettings, Field


class BaseSettings(BaseSettings):
    """Base settings using pydantic."""

    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8085)
    RELOAD: bool = Field(default=True)
    DEBUG: bool = Field(default=True)

    class Config:
        env_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True


class DevelopmentSettings(BaseSettings):
    """Development settings."""

    class Config:
        env_prefix = "DEV_"


class ProductionSettings(BaseSettings):
    """Production settings."""

    class Config:
        env_prefix = "PROD_"


class LocalSettings(BaseSettings):
    """Local settings."""

    class Config:
        env_prefix = "LOCAL_"


def get_settings(env="dev") -> BaseSettings:
    """Settings factory method."""

    settings = {
        "dev": DevelopmentSettings,
        "prod": ProductionSettings,
        "local": LocalSettings,
    }
    return settings[env]()
