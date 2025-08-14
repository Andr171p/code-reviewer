from collections.abc import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dishka import Provider, Scope, from_context, make_async_container, provide
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.redis import AsyncRedisSaver
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore

from .agent.workflow import Agent, build_graph
from .agent.nodes import DeveloperNode
from .constants import TOP_N
from .settings import Settings, settings


class AppProvider(Provider):
    app_settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_embeddings(self, app_settings: Settings) -> Embeddings:  # noqa: PLR6301
        return HuggingFaceEmbeddings(
            model_name=app_settings.embeddings.model_name,
            model_kwargs=app_settings.embeddings.model_kwargs,
            encode_kwargs=app_settings.embeddings.encode_kwargs,
        )

    @provide(scope=Scope.APP)
    def get_bot(self, config: Settings) -> Bot:
        return Bot(
            token=config.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
        )

    @provide(scope=Scope.APP)
    def get_model(self, app_settings: Settings) -> BaseChatModel:  # noqa: PLR6301
        return GigaChat(
            credentials=app_settings.gigachat.api_key,
            scope=app_settings.gigachat.scope,
            model=app_settings.gigachat.model_name,
            verify_ssl_certs=False,
            profanity_check=False,
        )

    @provide(scope=Scope.APP)
    def get_vectorstore(self, app_settings: Settings, embeddings: Embeddings) -> VectorStore:
        return PineconeVectorStore(
            embedding=embeddings,
            index_name="1c-best-practice",
            pinecone_api_key=app_settings.pinecone.api_key,
        )

    @provide(scope=Scope.APP)
    def get_developer_node(
            self, vectorstore: VectorStore, model: BaseChatModel
    ) -> DeveloperNode:
        return DeveloperNode(
            retriever=vectorstore.as_retriever(k=TOP_N), model=model
        )

    @provide(scope=Scope.APP)
    async def get_agent(  # noqa: PLR6301
        self,
            app_settings: Settings,
            developer_node: DeveloperNode,
    ) -> AsyncIterable[Agent]:
        ttl_config: dict[str, int | bool] = {
            "default_ttl": 60,  # Default TTL in minutes
            "refresh_on_read": True,  # Refresh TTL when checkpoint is read
        }
        async with AsyncRedisSaver(
                redis_url=app_settings.redis.url, ttl=ttl_config
        ) as checkpointer:
            yield build_graph(developer_node, checkpointer=checkpointer)


container = make_async_container(AppProvider(), context={Settings: settings})
