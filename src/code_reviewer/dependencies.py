from collections.abc import AsyncIterable

from dishka import Provider, Scope, from_context, make_async_container, provide
from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel
from langchain_core.vectorstores import VectorStore
from langchain_gigachat import GigaChat
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from langgraph.checkpoint.redis import AsyncRedisSaver
from langgraph.graph.state import CompiledStateGraph

from .agent.nodes import ReviewerNode
from .agent.states import AgentState
from .agent.workflow import build_graph
from .settings import Settings, settings


class AppProvider(Provider):
    app_settings = from_context(provides=settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_embeddings(self, app_settings: Settings) -> Embeddings:  # noqa: PLR6301
        return HuggingFaceEmbeddings(
            model_name=app_settings.embeddings.model_name,
            model_kwargs=app_settings.embeddings.model_kwargs,
            encode_kwargs=app_settings.embeddings.encode_kwargs,
        )

    @provide(scope=Scope.APP)
    def get_vectorstore(  # noqa: PLR6301
        self, app_settings: Settings, embeddings: Embeddings
    ) -> VectorStore:
        return PineconeVectorStore(
            embedding=embeddings,
            pinecone_api_key=app_settings.pinecone.api_key,
            index_name="1c-best-practice",
        )

    @provide(scope=Scope.APP)
    def get_model(self, app_settings: Settings) -> BaseChatModel:  # noqa: PLR6301
        return GigaChat(
            credentials=app_settings.gigachat.api_key,
            scope=app_settings.gigachat.scope,
            model=app_settings.gigachat.model,
            verify_ssl_certs=False,
            profanity_check=False,
        )

    @provide(scope=Scope.APP)
    async def get_agent(  # noqa: PLR6301
        self, app_settings: Settings, vectorstore: VectorStore, model: BaseChatModel
    ) -> AsyncIterable[CompiledStateGraph[AgentState]]:
        async with AsyncRedisSaver(redis_url=app_settings.redis.url) as checkpointer:
            yield build_graph(
                reviewer=ReviewerNode(vectorstore=vectorstore, model=model),
                checkpointer=checkpointer,
            )


container = make_async_container(AppProvider(), context={Settings: settings})
