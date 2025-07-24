from typing import Callable, Iterable, Any

import pymupdf4llm

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ContextEnrichmentSplitter:
    def __init__(
            self,
            chunk_size: int,
            chunk_overlap: int,
            length_function: Callable[[Iterable[Any]], int]
    ) -> None:
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=length_function
        )

    def split_documents(self, text: str) -> list[Document]:
        chunks = self._recursive_splitter.split_text(text)
        documents: list[Document] = []
        index = 0
        for chunk in chunks:
            documents.append(Document(page_content=chunk, metadata={"index": index}))
            index += 1
        return documents


pdf_path = (
    r"C:\Users\andre\CodeReviewer\Радченко_М_Г_,_Хрусталева_Е_Ю_1С_Предприятие_8_3_Практическое_пособие.pdf"
)

md_text = pymupdf4llm.to_markdown(pdf_path)

splitter = ContextEnrichmentSplitter(chunk_size=500, chunk_overlap=20, length_function=len)

docs = splitter.split_documents(md_text)

print(docs)
print(docs[5:])
