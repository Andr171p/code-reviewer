from pathlib import Path
import pytz

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
TIMEZONE = "Europe/Moscow"
moscow_tz = pytz.timezone(TIMEZONE)

load_dotenv(ENV_PATH)


class WeaviateSettings(BaseSettings):
    http_host: str = "localhost"
    http_port: int = 8080
    grpc_host: str = "localhost"
    grpc_port: int = 50051

    model_config = SettingsConfigDict(env_prefix="WEAVIATE_")


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class GigaChatSettings(BaseSettings):
    api_key: str = ""
    scope: str = ""
    model_name: str = "GigaChat:latest"

    model_config = SettingsConfigDict(env_prefix="GIGACHAT_")


class Settings(BaseSettings):
    weaviate: WeaviateSettings = WeaviateSettings()
    redis: RedisSettings = RedisSettings()
    gigachat: GigaChatSettings = GigaChatSettings()


settings = Settings()
