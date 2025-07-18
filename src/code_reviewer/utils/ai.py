from typing import TypeVar

from pydantic import BaseModel

from langchain_core.runnables import Runnable
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser

T = TypeVar("T", bound=BaseModel)


def create_llm_chain_with_structured_output(
    output_schema: type[T],
    llm:   BaseChatModel,
    prompt_template: str  
) -> Runnable[dict[str, str], T]:
    """Creating chain of callings with structured pydantic output.

    Args:
        output_schema (type[T]): Type of excepted chain output pydantic schema.
        llm (BaseChatModel): LLM for calling.
        prompt_template (str): Prompt template with instructions for LLM, required `format_instructions` value.

    Returns:
        Runnable[dict[str, str], T]: Built chain.
    """
    parser = PydanticOutputParser(pydantic_object=output_schema)
    prompt = (
        ChatPromptTemplate.from_messages([("system", prompt_template)])
        .partial(format_instructions=parser.get_format_instructions())
    )
    return prompt | llm | parser


def create_llm_chain(
    prompt_template: str, 
    llm: BaseChatModel
) -> Runnable[dict[str, str], str]:
    """Creating simple LLM chain.

    Args:
        prompt_template (str): Prompt template for giving instructions to model.
        llm (BaseChatModel): Model for calling.

    Returns:
        Runnable[dict[str, str], str]: Built chain.
    """
    return ChatPromptTemplate.from_template(prompt_template) | llm | StrOutputParser()
