from typing import Optional, Callable, Sized
from functools import cached_property

import spacy

from pydantic import BaseModel, Field

from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel

from langchain_text_splitters import (
    TextSplitter,
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter
)

from .schemas import EnrichmentTextChunk, EnrichmentWithHeadersTextChunk
from .constants import NER_MODEL, HEADERS_TO_SPLIT_ON
from .prompts import (
    TITLE_GENERATION_PROMPT, 
    KEYWORDS_EXTRACTION_PROMPT, 
    SUMMARIZATION_PROMPT,
)

from ...utils.ai import create_llm_chain, create_llm_chain_with_structured_output


def extract_keywords_using_nlp(text: str, nlp: spacy.Language) -> list[str]:
    return [token.text for token in nlp(text) if token.pos_ in ["NOUN", "PROPN"]]


def extract_keywords_using_llm(text: str, llm: BaseChatModel) -> list[str]:
    class ExtractedKeywords(BaseModel):
        keywords: list[str] = Field(..., description="Ключевые слова для поиска.")

    llm_chain = create_llm_chain_with_structured_output(
        output_schema=ExtractedKeywords,
        prompt_template=KEYWORDS_EXTRACTION_PROMPT,
        llm=llm
    )
    extracted = llm_chain.invoke({"text": text})
    return extracted.keywords


class MarkdownEnrichmentTextSplitter(TextSplitter):
    """
        Text splitter for Markdown documents with additional chunk enriched.

        This splitter does:
        1. Dividing a Markdown document by headings (h1-h6).
        2. Additional recursive change on cups of the displayed size.
        3. Enriched of each chunk:
            - Header generation.
            - Creating a summary.
            - Keywords extraction (using NLP or LLM)

        Args:
            chunk_size (int): Max size of chunk in characters.
            chunk_overlap (int): Overlap between adjacent chunks in characters.
            length_function: (Callable[[Sized], int]): Function for computing length of text.
            llm: (BaseChatModel): LLM model for title generation, summarization and keyword extraction.
            use_md_headers_splitter: (bool, optional): Using Markdown splitting by headers.
            use_llm_for_ner: (bool, optional): Using LLM for keyword extraction, default False.
            ner_model: (str, optional): NER model for keyword extraction, default None.
    """
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[[Sized], int],
            llm: BaseChatModel,
            use_md_headers_splitter: bool = False,
            use_llm_for_ner: bool = False,
            ner_model: Optional[str] = None
    ) -> None:
        super().__init__(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )
        self._llm = llm
        self._use_llm_for_ner = use_llm_for_ner
        self._ner_model = ner_model if ner_model else NER_MODEL
        self._use_md_headers_splitter = use_md_headers_splitter
        self._headers_to_split_on = HEADERS_TO_SPLIT_ON
        self._markdown_splitter = MarkdownHeaderTextSplitter(self._headers_to_split_on)
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )

    @cached_property
    def _nlp(self) -> spacy.Language:
        return spacy.load(self._ner_model)

    def split_text(self, text: str) -> list[str]:
        if not text.strip():
            raise ValueError("Text must be not empty!")
        if self._use_md_headers_splitter:
            documents = self._markdown_splitter.split_text(text)
        else:
            documents = [Document(page_content=text)]
        title = self._generate_title(text)
        enriched_chunks: list[str] = []
        for document in documents:
            headers = document.metadata
            chunks = self._recursive_splitter.split_text(document.page_content)
            for chunk in chunks:
                enriched_chunk = self._enrich_chunk(title, headers, chunk)
                enriched_chunks.append(enriched_chunk)
        return enriched_chunks

    def _enrich_chunk(
            self,
            title: str,
            headers: Optional[dict[str, str]],
            content: str
    ) -> str:
        summary = self._summarize(content)
        keywords = self._extract_keywords(content)
        params: dict[str, str] = {
            "title": title,
            "content": content,
            "summary": summary,
            "keywords": keywords
        }
        if headers:
            for key, value in headers.items():
                params[key] = headers.get(value)
            chunk = EnrichmentWithHeadersTextChunk(**params)
        else:
            chunk = EnrichmentTextChunk(**params)
        return chunk.to_text()

    def _generate_title(self, text: str) -> str:

        class GeneratedTitle(BaseModel):
            title: str = Field(..., description="Заголовок или основная тема текста.")

        llm_chain = create_llm_chain_with_structured_output(
            output_schema=GeneratedTitle,
            prompt_template=TITLE_GENERATION_PROMPT,
            llm=self._llm
        )
        generated = llm_chain.invoke({"text": text})
        return generated.title

    def _summarize(self, text: str) -> str:
        llm_chain = create_llm_chain(
            prompt_template=SUMMARIZATION_PROMPT, llm=self._llm
        )
        summary = llm_chain.invoke({"text": text})
        return summary

    def _extract_keywords(self, text: str) -> list[str]:
        if self._use_llm_for_ner:
            keywords = extract_keywords_using_llm(text, llm=self._llm)
        else:
            keywords = extract_keywords_using_nlp(text, nlp=self._nlp)
        return keywords
