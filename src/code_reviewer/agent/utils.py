from typing import TypeVar

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def create_llm_chain_with_structured_output[T](
    output_schema: type[T],
    llm: BaseChatModel,
    prompt: str,
) -> Runnable[dict[str, str], T]:
    """Creating chain of callings with structured pydantic output.

    Args:
        output_schema (type[T]): Type of excepted chain output pydantic schema.
        llm (BaseChatModel): LLM for calling.
        prompt (str): Prompt template with instructions for LLM, required `format_instructions` value.

    Returns:
        Runnable[dict[str, str], T]: Built chain.
    """  # noqa: E501
    parser = PydanticOutputParser(pydantic_object=output_schema)
    prompt = ChatPromptTemplate.from_messages([("system", prompt)]).partial(
        format_instructions=parser.get_format_instructions(),
    )
    return prompt | llm | parser


def create_llm_chain(prompt: str, llm: BaseChatModel) -> Runnable[dict[str, str], str]:
    """Creating simple LLM chain.

    Args:
        prompt (str): Prompt template for giving instructions to model.
        llm (BaseChatModel): Model for calling.

    Returns:
        Runnable[dict[str, str], str]: Built chain.
    """
    return ChatPromptTemplate.from_template(prompt) | llm | StrOutputParser()


def format_documents(documents: list[Document]) -> str:
    return "\n\n".join([document.page_content for document in documents])
