import pymupdf4llm

from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter


splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("*", "h1"), ("**", "h2"), ("***", "h3")
    ],
    strip_headers=False
)

pdf_path = r"C:\Users\andre\CodeReviewer\Радченко_М_Г_,_Хрусталева_Е_Ю_1С_Предприятие_8_3_Практическое_пособие.pdf"

md_text = pymupdf4llm.to_markdown(pdf_path)

print(md_text)

docs = splitter.split_text(md_text)

print(len(docs))
print(docs[5:])
