from pathlib import Path

import pytz
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
TIMEZONE = "Europe/Moscow"
moscow_tz = pytz.timezone(TIMEZONE)

load_dotenv(ENV_PATH)


class BotSettings(BaseSettings):
    token: str = ""

    model_config = SettingsConfigDict(env_prefix="BOT_")


class GitHubSettings(BaseSettings):
    access_token: str = ""

    model_config = SettingsConfigDict(env_prefix="GITHUB_")


class EmbeddingsSettings(BaseModel):
    model_name: str = "deepvk/USER-bge-m3"
    model_kwargs: dict[str, str] = {"device": "cpu"}
    encode_kwargs: dict[str, bool] = {"normalize_embeddings": False}


class WeaviateSettings(BaseSettings):
    http_host: str = "localhost"
    http_port: int = 8080
    grpc_host: str = "localhost"
    grpc_port: int = 50051

    model_config = SettingsConfigDict(env_prefix="WEAVIATE_")


class PineconeSettings(BaseSettings):
    api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="PINECONE_")


class ElasticSettings(BaseSettings):
    host: str = "localhost"
    port: int = 9200
    username: str = "user"
    password: str = "password"

    model_config = SettingsConfigDict(env_prefix="ELASTIC_")

    @property
    def url(self) -> str:
        return f"http://{self.host}:{self.port}"

    @property
    def auth(self) -> tuple[str, str]:
        return self.username, self.password


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
    bot: BotSettings = BotSettings()
    github: GitHubSettings = GitHubSettings()
    embeddings: EmbeddingsSettings = EmbeddingsSettings()
    weaviate: WeaviateSettings = WeaviateSettings()
    pinecone: PineconeSettings = PineconeSettings()
    redis: RedisSettings = RedisSettings()
    elastic: ElasticSettings = ElasticSettings()
    gigachat: GigaChatSettings = GigaChatSettings()


settings = Settings()
