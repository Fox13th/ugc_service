import os
from functools import lru_cache

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_file_path = '.env'
if not os.path.exists(env_file_path):
    raise TypeError(f'Env file not found. Path: "{env_file_path}"')
load_dotenv(dotenv_path=env_file_path)


class Settings(BaseSettings):
    # App Settings
    project_name: str = 'static_service'
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Kafka Settings
    kafka_host: str = '127.0.0.1'
    kafka_port: str = '9094'
    kafka_topic: str = 'events'

    secret_key: str = 'secret'
    debug: bool = False

    jwt_secret: str = 'test-secret'

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache(maxsize=None)
def get_settings():
    """Получаем настройки приложения, сохраняя в кэш."""
    return Settings(_env_file=env_file_path)
