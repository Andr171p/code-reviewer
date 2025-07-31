from langchain_gigachat import GigaChat
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.redis import AsyncRedisSaver

from .toolkits import RedisLongTermMemoryToolkit, WeaviateSearchToolkit
from .prompts import CODE_REVIEW_PROMPT

GIGACHAT_API_KEY = "NTJlZTEzZjYtYmUyYy00ZWY2LTllNDMtYWM2YjBjYmM1ODU1OmEzMzIwMmE1LWNkOWMtNGQ4MS05OTNjLWI1Mjk4Mzc4YzUzNw=="
GIGACHAT_SCOPE = "GIGACHAT_API_B2B"
GIGACHAT_MODEL = "GigaChat-2-Pro"

gigachat_pro = GigaChat(
    credentials=GIGACHAT_API_KEY,
    scope=GIGACHAT_SCOPE,
    model=GIGACHAT_MODEL,
    verify_ssl_certs=False,
    profanity_check=False
)

memory_toolkit = RedisLongTermMemoryToolkit(
    url="redis://10.1.50.85:8379", hf_vectorizer_model="deepvk/USER-bge-m3"
)

search_toolkit = WeaviateSearchToolkit(
    connection_params={
        "http_host": "10.1.50.85",
        "http_port": 8090,
        "http_secure": False,
        "grpc_host": "10.1.50.85",
        "grpc_port": 50051,
        "grpc_secure": False
    },
    hf_embeddings_model="deepvk/USER-bge-m3"
)

tools: list[BaseTool] = [
    *memory_toolkit.get_tools(),
    *search_toolkit.get_tools()
]


async def chat(query: str) -> ...:
    thread_id = "12345"
    user_id = "123"
    async with AsyncRedisSaver.from_conn_string(
            "redis://10.1.50.85:8379"
    ) as checkpointer:
        config = RunnableConfig(configurable={"thread_id": thread_id, "user_id": user_id})
        agent = create_react_agent(
            model=gigachat_pro,
            prompt=CODE_REVIEW_PROMPT,
            tools=tools,
            checkpointer=checkpointer
        )
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}, config=config
        )
    print(response)
