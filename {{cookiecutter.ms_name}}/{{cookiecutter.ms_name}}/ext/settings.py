import os
import pathlib
from functools import lru_cache


class BaseConfig:

    EXTENSIONS = ["{{cookiecutter.ms_name}}.routers.v1",
                  "{{cookiecutter.ms_name}}.ext.cors", "{{cookiecutter.ms_name}}.ext.database"]


class DevelopmentConfig(BaseConfig):
    DATABASE_URL: str = "postgresql+asyncpg://{{cookiecutter.ms_name}}:{{cookiecutter.ms_name}}@db:5432/{{cookiecutter.ms_name}}"
    DATABASE_CONNECT_DICT: dict = {}
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ALGORITHM = os.environ.get("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_HOURS = os.environ.get("ACCESS_TOKEN_EXPIRE_HOURS")
    pass


class ProductionConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get("SQLALCHEMY_DATABASE_URI")
    DATABASE_CONNECT_DICT: dict = {}
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("FASTAPI_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
