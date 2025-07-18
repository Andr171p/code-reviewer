from __future__ import annotations
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter

from ..core.enums import ProgramingLanguage

from .constants import LANGUAGE2SEPARATORS, ENRICHED_CHUNK_TEMPLATE
from .prompts import SUMMARIZER_PROMPT


class CodeEnrichmentSplitter(TextSplitter):
    def __init__(
            self,
            language: ProgramingLanguage,
            llm: BaseChatModel,
            **kwargs
    ) -> None:
        """Initialize the code splitter with language-specific rules.
        
        Args:
            language: Programming language of the code to split
            llm: Language model for generating chunk descriptions
            kwargs: Additional arguments for TextSplitter
            
        Raises:
            ValueError: If language is not supported
        """
        super().__init__(**kwargs)
        self._language = language
        self._separators = LANGUAGE2SEPARATORS.get(self._language)
        if not self._separators:
            raise ValueError(f"Language {language} is not implemented yet!")
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            separators=self._separators, **kwargs
        )
        self._llm = llm

    def split_text(self, text: str) -> list[str]:
        chunks = self._recursive_splitter.split_text(text)
        enriched_chunks = [
            ENRICHED_CHUNK_TEMPLATE.format(
                filename=...,
                content=chunk,
                description=self._get_code_description(chunk),
                language=self._language
            )
            for chunk in chunks
        ]
        return enriched_chunks

    def _get_code_description(
        self, content: str, metadata: Optional[dict[str, str]] = None
        ) -> str:
        """_summary_

        Args:
            content (str): Code content
            metadata (Optional[dict[str, str]], optional): Additional info about code.

        Returns:
            str: Generated code description.
        """
        llm_chain = (
            ChatPromptTemplate.from_template(SUMMARIZER_PROMPT) 
            | self._llm 
            | StrOutputParser()
        )
        description = llm_chain.invoke({
            "content": content, "metadata": metadata
        })
        return description
