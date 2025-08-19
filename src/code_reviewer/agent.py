from __future__ import annotations

from typing import Callable

import logging
from dataclasses import dataclass
from enum import StrEnum

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from .prompts import (
    ASSISTANT_PROMPT,
    CODE_REVIEW_PROMPT,
    DEVELOPER_PROMPT,
    HYPOTHETICAL_CODE_GENERATION_PROMPT,
    ROUTE_PROMPT,
    GENERAL_PROMPT,
)
from .utils import (
    create_chain,
    create_chain_with_structured_output,
    create_rag_chain,
    format_documents,
    format_messages
)
from .memory import RedisChatHistory
from .dependencies import container
from .constants import TOP_N

logger = logging.getLogger(__name__)


@dataclass
class State:
    """Состояние графа"""
    messages: list[BaseMessage]


@dataclass
class Dependencies:
    """Зависимости графа"""
    vectorstore_factory: Callable[[str], VectorStore]
    llm: BaseChatModel


class NextNode(StrEnum):
    DEVELOPER = "developer"
    CODE_REVIEW = "code_review"
    ASSISTANT = "assistant"
    GENERAL = "general"


class Routing(BaseModel):
    next_node: NextNode = Field(
        description="Следующий агент которому нужно передать запрос"
    )


@dataclass
class RoutingNode(BaseNode[State, Dependencies]):
    async def run(
            self, ctx: GraphRunContext[State, Dependencies]
    ) -> WritingCodeNode | CodeReviewNode | AskAssistantNode | End:
        chain = create_chain_with_structured_output(
            output_type=Routing,
            prompt=ROUTE_PROMPT,
            llm=ctx.deps.llm,
        )
        chat_prompt = format_messages(ctx.state.messages)
        user_prompt = ctx.state.messages[-1].content
        routing = await chain.ainvoke({"query": chat_prompt})
        logger.info("Route to %s", routing.next_node)
        if routing.next_node == NextNode.DEVELOPER:
            return WritingCodeNode(user_prompt)
        elif routing.next_node == NextNode.CODE_REVIEW:
            return CodeReviewNode(user_prompt)
        elif routing.next_node == NextNode.ASSISTANT:
            return AskAssistantNode(chat_prompt)
        else:
            chain = create_chain(prompt=GENERAL_PROMPT, llm=ctx.deps.llm)
            ai_message = await chain.ainvoke({"query": chat_prompt})
            ctx.state.messages.append(ai_message)
            return End(None)


@dataclass
class AskAssistantNode(BaseNode[State, Dependencies]):
    chat_prompt: str

    async def run(
            self, ctx: GraphRunContext[State, Dependencies]
    ) -> End:
        logger.info("Ask assistant agent")
        assistant_chain = create_rag_chain(
            vectorstore=ctx.deps.vectorstore_factory("1c-best-practice"),
            prompt=ASSISTANT_PROMPT,
            llm=ctx.deps.llm,
        )
        ai_message = await assistant_chain.ainvoke(self.chat_prompt)
        ctx.state.messages.append(ai_message)
        return End(None)


@dataclass
class CodeReviewNode(BaseNode[State, Dependencies]):
    user_prompt: str

    async def run(
            self, ctx: GraphRunContext[State, Dependencies]
    ) -> End:
        logger.info("Start code review")
        code_review_chain = create_rag_chain(
            vectorstore=ctx.deps.vectorstore_factory("1c-best-practice"),
            prompt=CODE_REVIEW_PROMPT,
            llm=ctx.deps.llm,
        )
        ai_message = await code_review_chain.ainvoke(self.user_prompt)
        ctx.state.messages.append(ai_message)
        return End(None)


@dataclass
class WritingCodeNode(BaseNode[State, Dependencies]):
    user_prompt: str

    async def run(
            self, ctx: GraphRunContext[State, Dependencies]
    ) -> End:
        logger.info("Generate code")
        hypothetical_chain = create_chain(
            prompt=HYPOTHETICAL_CODE_GENERATION_PROMPT, llm=ctx.deps.llm
        )
        hypothetical_message = await hypothetical_chain.ainvoke({"query": self.user_prompt})
        documents = await ctx.deps.vectorstore_factory("1c-code").asimilarity_search(
            query=hypothetical_message.content, k=TOP_N
        )
        prompt = DEVELOPER_PROMPT.format(
            context=format_documents(documents), query=self.user_prompt
        )
        developer_chain = create_chain(prompt=prompt, llm=ctx.deps.llm)
        developer_message = await developer_chain.ainvoke({
            "query": self.user_prompt,
        })
        ctx.state.messages.append(developer_message)
        return End(None)


async def run_agent(chat_id: str, user_prompt: str) -> str:
    vectorstore_factory = await container.get(Callable[[str], VectorStore])
    llm = await container.get(BaseChatModel)
    chat_history = await container.get(RedisChatHistory)
    messages = await chat_history.get_messages(chat_id)
    messages.append(HumanMessage(content=user_prompt))
    state = State(messages=messages)
    deps = Dependencies(vectorstore_factory=vectorstore_factory, llm=llm)
    graph = Graph(nodes=(RoutingNode, CodeReviewNode, WritingCodeNode, AskAssistantNode))
    result = await graph.run(RoutingNode(), state=state, deps=deps)
    ai_message = result.state.messages[-1]
    await chat_history.add_messages(chat_id, [ai_message])
    return ai_message.content
