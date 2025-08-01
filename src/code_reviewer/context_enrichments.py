from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

from .constants import GITHUB_API_BASE_URL
from src.code_reviewer.agent.utils import create_llm_chain_with_structured_output

DESCRIPTION_GENERATOR_PROMPT = """\
Ты опытный разработчик 1С, анализирующий модуль BSL. Сгенерируй краткое, но информативное описание назначения модуля (2-3 предложения) по следующим правилам:

1. Определи тип модуля (обработка, отчет, общий модуль, менеджер и т.д.)
2. Выдели ключевую функциональность
3. Укажи основные сущности/объекты 1С, с которыми работает модуль
4. Отметь специфичные особенности (если есть)

Данные для анализа:
- Проект: {project}
- Имя модуля: {filename}
- Путь в проекте: {path}
- Код модуля: {content}

Верните ответ в виде ВАЛИДНОГО JSON со следующей структурой:
{format_instructions}
"""


def get_github_repo_name(repo_url: str) -> str:
    repo_url = repo_url.replace(GITHUB_API_BASE_URL, "")
    parts = repo_url.split("/")
    return f"{parts[1]}/{parts[2]}"


class ModuleDescription(BaseModel):
    type: str = Field(description="Тип модуля")
    purpose: str = Field(description="Основное назначение модуля")
    details: str = Field(default="", description="Дополнительные детали")


class BSLGithubContextEnricher:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm

    def enrich_documents(self, documents: list[Document]) -> list[Document]:
        enriched_documents: list[Document] = []
        for document in documents:
            content = document.page_content
            metadata: dict[str, str] = {
                "source": document.metadata.get("source"),
                "project": get_github_repo_name(document.metadata["source"]),
                "filename": document.metadata.get("path").split("/")[-1],
                "path": document.metadata.get("path")
            }
            description = self._generate_description(content, metadata)
            metadata.update({
                "type": description.type,
                "purpose": description.purpose,
                "detail": description.details
            })
            enriched_documents.append(Document(page_content=content, metadata=metadata))
        return enriched_documents

    def _generate_description(
            self, content: str, metadata: dict[str, str]
    ) -> ModuleDescription:
        llm_chain = create_llm_chain_with_structured_output(
            output_schema=ModuleDescription,
            prompt_template=DESCRIPTION_GENERATOR_PROMPT,
            llm=self.llm
        )
        description = llm_chain.invoke({
            "project": metadata.get("project", ""),
            "filename": metadata.get("filename", ""),
            "path": metadata.get("path", ""),
            "content": content
        })
        return description


ENRICHMENT_PAGE_CONTENT = """**Проект**: {project}
**Имя модуля**: {filename}
**Путь до модуля в проекте**: {path}
**Часть кода модуля**: {content}
**Тип модуля**: {type}
**Основная задача модуля**: {purpose}
**Дополнительные детали**: {detail}
"""


def enrich_page_content(document: Document) -> Document:
    enrichment_page_content = ENRICHMENT_PAGE_CONTENT.format(
        content=document.page_content, **document.metadata
    )
    return Document(page_content=enrichment_page_content)
