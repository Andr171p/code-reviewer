from typing import TypeVar

from collections.abc import Sequence

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnablePassthrough, RunnableSerializable
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel

from src.code_reviewer.constants import TOP_N

T = TypeVar("T", bound=BaseModel)


def create_chain_with_structured_output[T](
    output_type: type[T],
    llm: BaseChatModel,
    prompt: str,
) -> Runnable[dict[str, str], T]:
    parser = PydanticOutputParser(pydantic_object=output_type)
    prompt = ChatPromptTemplate.from_messages([("system", prompt)]).partial(
        format_instructions=parser.get_format_instructions(),
    )
    return prompt | llm | parser


def create_chain(prompt: str, llm: BaseChatModel) -> Runnable[dict[str, str], BaseMessage]:
    return ChatPromptTemplate.from_template(prompt) | llm


def create_rag_chain(
    vectorstore: VectorStore, prompt: str, llm: BaseChatModel
) -> RunnableSerializable[str, BaseMessage]:
    return (
        {
            "context": vectorstore.as_retriever(k=TOP_N) | format_documents,
            "query": RunnablePassthrough(),
        }
        | ChatPromptTemplate.from_template(prompt)
        | llm
    )


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])


def format_messages(messages: Sequence[BaseMessage]) -> str:
    return "\n\n".join(
        f"{'User' if isinstance(message, HumanMessage) else 'AI'}: {message.content}"
        for message in messages
    )
