from langchain_gigachat import GigaChat
from langchain_core.tools import BaseTool
from langgraph.prebuilt import create_react_agent

from .toolkits import RedisLongTermMemoryToolkit, WeaviateSearchToolkit
from .prompts import CODE_REVIEW_PROMPT

gigachat_pro = GigaChat(
    credentials="",
    scope="",
    model="",
    verify_ssl_certs=False,
    profanity_check=False
)

memory_toolkit = RedisLongTermMemoryToolkit(
    url="", hf_vectorizer_model=""
)

search_toolkit = WeaviateSearchToolkit(
    connection_params={}, hf_embeddings_model=""
)

tools: list[BaseTool] = [
    *memory_toolkit.get_tools(),
    *search_toolkit.get_tools()
]

agent = create_react_agent(
    model=gigachat_pro,
    prompt=CODE_REVIEW_PROMPT,
    tools=tools,
)
