from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from enum import StrEnum

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field
from pydantic_graph import BaseNode, End, Graph, GraphRunContext

from src.code_reviewer.agent.prompts import (
    ASSISTANT_PROMPT,
    CODE_REVIEW_PROMPT,
    DEVELOPER_PROMPT,
    HYPOTHETICAL_CODE_GENERATION_PROMPT,
    ROUTE_PROMPT,
)
from src.code_reviewer.agent.utils import (
    create_chain,
    create_chain_with_structured_output,
    create_rag_chain,
    format_documents,
)
from src.code_reviewer.constants import TOP_N

logger = logging.getLogger(__name__)


@dataclass
class AgentState:
    messages: list[BaseMessage] = field(default_factory=list)


@dataclass
class Dependencies:
    vectorstore: VectorStore
    llm: BaseChatModel


class NextNode(StrEnum):
    DEVELOPER = "developer"
    CODE_REVIEW = "code_review"
    ASSISTANT = "assistant"


class Routing(BaseModel):
    next_node: NextNode = Field(
        description="Следующий агент которому нужно передать запрос"
    )


@dataclass
class RoutingNode(BaseNode[AgentState, Dependencies]):
    async def run(
            self, ctx: GraphRunContext[AgentState, Dependencies]
    ) -> DeveloperNode | CodeReviewNode | AssistantNode:
        chain = create_chain_with_structured_output(
            output_type=Routing,
            prompt=ROUTE_PROMPT,
            llm=ctx.deps.llm,
        )
        query = ctx.state.messages[-1].content
        routing = await chain.ainvoke({"query": query})
        logger.info(
            "===========ROUTE TO %s===========", routing.next_node.upper()
        )
        if routing.next_node == NextNode.DEVELOPER:
            return DeveloperNode(query=query)
        if routing.next_node == NextNode.CODE_REVIEW:
            return CodeReviewNode(query=query)
        return AssistantNode(query=query)


@dataclass
class AssistantNode(BaseNode[AgentState, Dependencies]):
    query: str

    async def run(
            self, ctx: GraphRunContext[AgentState, Dependencies]
    ) -> End:
        logger.info("===========RUN ASSISTANT===========")
        assistant_chain = create_rag_chain(
            vectorstore=ctx.deps.vectorstore,
            prompt=ASSISTANT_PROMPT,
            llm=ctx.deps.llm,
        )
        assistant_message = await assistant_chain.ainvoke(self.query)
        ctx.state.messages.append(assistant_message)
        return End(None)


@dataclass
class CodeReviewNode(BaseNode[AgentState, Dependencies]):
    query: str

    async def run(
            self, ctx: GraphRunContext[AgentState, Dependencies]
    ) -> End:
        logger.info("===========START CODE REVIEW===========")
        code_review_chain = create_rag_chain(
            vectorstore=ctx.deps.vectorstore,
            prompt=CODE_REVIEW_PROMPT,
            llm=ctx.deps.llm,
        )
        ai_message = await code_review_chain.ainvoke(self.query)
        ctx.state.messages.append(ai_message)
        return End(None)


@dataclass
class DeveloperNode(BaseNode[AgentState]):
    query: str

    async def run(
            self, ctx: GraphRunContext[AgentState, Dependencies]
    ) -> End:
        logger.info("===========START CODE GENERATION===========")
        hypothetical_chain = create_chain(
            prompt=HYPOTHETICAL_CODE_GENERATION_PROMPT, llm=ctx.deps.llm
        )
        hypothetical_message = await hypothetical_chain.ainvoke({
            "query": self.query
        })
        documents = await ctx.deps.vectorstore.asimilarity_search(
            query=hypothetical_message.content, k=TOP_N
        )
        print(format_documents(documents))
        prompt = DEVELOPER_PROMPT.format(
            context=format_documents(documents), query=self.query
        )
        developer_chain = create_chain(prompt=prompt, llm=ctx.deps.llm)
        developer_message = await developer_chain.ainvoke({
            "query": self.query
        })
        ctx.state.messages.append(developer_message)
        return End(None)


user_query = """&НаКлиенте
Процедура ОтправитьЗапрос(Команда)
 Соединение = Новый HTTPСоединение("10.1.50.109", 8000);
 HTTPЗапрос = Новый HTTPЗапрос("/api/v1/tasks/");
 
 JSON = Новый ЗаписьJSON;
 JSON.УстановитьСтроку();
 
 СтруктураРаботы = Новый Структура("hours, content", 5, "Создание формы");
 Массив = Новый Массив;
 Массив.Добавить(СтруктураРаботы);
 
 Структура = Новый Структура;
 Структура.Вставить("subdivision", "Кежуй");
 Структура.Вставить("theme", "Разработка");
 Структура.Вставить("description", "Настройка и доработка");
 Структура.Вставить("hours", 5);
 Структура.Вставить("jobs", Массив);
 
 ЗаписатьJSON(JSON, Структура);

 Результат = JSON.Закрыть();

 HTTPЗапрос.УстановитьТелоИзСтроки(Результат, "UTF-8");
 
 Ответ = Соединение.ОтправитьДляОбработки(HTTPЗапрос);
КонецПроцедуры


Напиши UNIT тест для этого кода
"""


async def main():
    from langchain_core.messages import HumanMessage

    from src.code_reviewer.dependencies import container

    vectorstore = await container.get(VectorStore)
    llm = await container.get(BaseChatModel)
    state = AgentState(messages=[HumanMessage(content=user_query)])
    deps = Dependencies(vectorstore=vectorstore, llm=llm)
    graph = Graph(nodes=(RoutingNode, CodeReviewNode, DeveloperNode, AssistantNode))
    result = await graph.run(RoutingNode(), state=state, deps=deps)
    print(result.state.messages[-1])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
