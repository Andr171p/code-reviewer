from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

from ..utils.chains import create_llm_chain_with_structured_output
from ..utils.converters import get_github_repo_name
from ..prompts import DESCRIPTION_GENERATOR_PROMPT


class ModuleDescription(BaseModel):
    type: str = Field(description="Тип модуля")
    purpose: str = Field(description="Основное назначение модуля")
    details: str = Field(default="", description="Дополнительные детали")


class BSLDocumentContextEnricher:
    def __init__(self, llm: BaseChatModel | None = None) -> None:
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
