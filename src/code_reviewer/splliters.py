from __future__ import annotations

from typing import Callable, Any
from collections.abc import Iterable, Sequence

from pydantic import Field

from llama_index.core.llms import LLM
from llama_index.core.schema import BaseNode
from llama_index.core.node_parser import NodeParser
from llama_index.core.utils import get_tqdm_iterable
from llama_index.core.node_parser import MarkdownNodeParser, LangchainNodeParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

DEFAULT_CHUNK_SIZE = 600
DEFAULT_CHUNK_OVERLAP = 20


class ContextEnrichmentMarkdownNodeParser(NodeParser):
    chunk_size: int = Field(
        default=DEFAULT_CHUNK_SIZE,
        description="Максимальный размер чанка в символах."
    )
    chunk_overlap: int = Field(
        default=DEFAULT_CHUNK_OVERLAP,
        description="Размер перекрытия чанков в символах."
    )
    length_function: Callable[[Iterable[Any]], int] = Field(
        default=len,
        description="Функция для вычисления длины чанка."
    )
    llm: LLM | None = Field(
        default=None,
        description="LLM для суммаризации и извлечения ключевых слов чанков."
    )

    @property
    def markdown_parser(self) -> MarkdownNodeParser:
        return MarkdownNodeParser(
            include_metadata=True,
            include_prev_next_rel=True
        )

    @property
    def recursive_parser(self) -> NodeParser:
        return LangchainNodeParser(
            RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=self.length_function
            )
        )

    @classmethod
    def class_name(cls) -> str:
        return "ContextEnrichmentMarkdownNodeParser"

    @classmethod
    def from_defaults(cls, ) -> ContextEnrichmentMarkdownNodeParser:
        ...

    def _parse_nodes(
            self,
            nodes: Sequence[BaseNode],
            show_progress: bool = False,
            **kwargs: Any
    ) -> list[BaseNode]:
        all_nodes: list[BaseNode] = []
        nodes_with_progress = get_tqdm_iterable(nodes, show_progress, "Parsing nodes")
        for node in nodes_with_progress:
            md_nodes = self.markdown_parser.get_nodes_from_node(node)
            enriched_md_nodes = self._enrich_context(md_nodes)

    @staticmethod
    def _enrich_context(nodes: Sequence[BaseNode]) -> list[BaseNode]:
        index = 0
        for node in nodes:
            node.metadata.update({
                "title": node.metadata.get("filename"),
                "header": node.metadata.get("header_path"),
                "summary": ...,
                "keywords": ...,
                "index": index
            })
        return nodes
