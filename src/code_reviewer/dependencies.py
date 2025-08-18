from typing import Callable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from dishka import Provider, Scope, from_context, make_async_container, provide
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.vectorstores import VectorStore
from langchain_pinecone import PineconeVectorStore

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
    def get_llm(self, app_settings: Settings) -> BaseChatModel:  # noqa: PLR6301
        return GigaChat(
            credentials=app_settings.gigachat.api_key,
            scope=app_settings.gigachat.scope,
            model=app_settings.gigachat.model_name,
            verify_ssl_certs=False,
            profanity_check=False,
        )

    @provide(scope=Scope.APP)
    def get_vectorstore_factory(
            self, app_settings: Settings, embeddings: Embeddings
    ) -> Callable[[str], VectorStore]:
        def vectorstore_factory(index_name: str) -> VectorStore:
            return PineconeVectorStore(
                embedding=embeddings,
                index_name=index_name,
                pinecone_api_key=app_settings.pinecone.api_key,
            )
        return vectorstore_factory


container = make_async_container(AppProvider(), context={Settings: settings})
