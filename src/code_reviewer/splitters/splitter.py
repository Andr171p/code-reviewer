from __future__ import annotations
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import TextSplitter, RecursiveCharacterTextSplitter

from .constants import ProgramingLanguage, LANGUAGE2SEPARATORS
from .prompts import SUMMARIZER_PROMPT


class EnrichedCodeSplitter(TextSplitter):
    def __init__(
            self,
            language: ProgramingLanguage,
            llm: BaseChatModel,
            **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self._separators = LANGUAGE2SEPARATORS.get(language)
        if not self._separators:
            raise ValueError(f"Language {language} is not implemented yet!")
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            separators=self._separators, **kwargs
        )
        self._llm = llm

    def split_text(self, text: str) -> list[str]:
        ...

    def _get_code_description(self, code: str, additional_info: Optional[dict[str, str]] = None) -> str:
        """Generate description for program code with additional data about project.

        :param code: Programming code
        :param additional_info: Additional information about project
        :return: Text of code snippet description
        """
        llm_chain = ChatPromptTemplate.from_template(SUMMARIZER_PROMPT) | self._llm | StrOutputParser()
        description = llm_chain.invoke({"code": code, "additional_info": additional_info})
        return description
