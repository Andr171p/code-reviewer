from langchain_core.language_models import BaseChatModel
from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from pydantic import BaseModel, Field

from ..core.enums import Language
from ..utils.ai import create_llm_chain_with_structured_output
from .constants import LANGUAGE2SEPARATORS, MIN_CHUNK_LENGTH
from .prompts import ENRICHER_PROMPT


class CodeSplitter(TextSplitter):
    def __init__(
            self,
            language: Language,
            enrich_chunks: bool = False,
            llm: BaseChatModel | None = None,
            additional_context: str = "",
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._language = language
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=self._chunk_overlap,
            length_function=self._length_function,
            separators=LANGUAGE2SEPARATORS.get(self._language)
        )
        self._enrich_chunks = enrich_chunks
        self._llm = llm
        self._additional_context = additional_context

    def split_text(self, text: str) -> list[str]:
        chunks = self._recursive_splitter.split_text(text)
        if self._enrich_chunks:
            enriched_chunks: list[str] = []
            for chunk in chunks:
                if len(chunk) > MIN_CHUNK_LENGTH:
                    enriched_chunk = self._enrich_context(chunk)
                    enriched_chunks.append(enriched_chunk)
                else:
                    enriched_chunks.append(chunk)
            return enriched_chunks
        return chunks

    def _enrich_context(self, text: str) -> str:
        class Enrichment(BaseModel):
            description: str = Field(
                description="Описание кода (для чего он нужен, какие проблемы решает и.т.д"
            )
            tags: str = Field(
                description="Теги для улучшения поиска по чанку с кодом"
            )
        llm_chain = create_llm_chain_with_structured_output(
            output_schema=Enrichment,
            prompt_template=ENRICHER_PROMPT,
            llm=self._llm,
            additional_context=self._additional_context
        )
        enrichment = llm_chain.invoke({"language": self._language, "text": text})
        return f"""**Код**:
        
        ```{self._language}
        {text}
        ```
        
        **Описание**: {enrichment.description}
        
        **Тэги**: {enrichment.tags}
        """
