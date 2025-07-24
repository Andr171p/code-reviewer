import pymupdf4llm

from llama_index.core import Document
from llama_index.core.node_parser import MarkdownNodeParser, LangchainNodeParser
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on)

md_parser = MarkdownNodeParser(include_metadata=True, include_prev_next_rel=True)

pdf_path = r"Радченко_М_Г_,_Хрусталева_Е_Ю_1С_Предприятие_8_3_Практическое_пособие.pdf"

md_text = pymupdf4llm.to_markdown(pdf_path)

# md_nodes = md_parser.get_nodes_from_documents([Document(text=md_text)])

md_nodes = markdown_splitter.split_text(md_text)

recursive_parser = LangchainNodeParser(
    RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=20,
        length_function=len
    )
)

all_nodes = ...

print(len(md_nodes))
'''
k = 0
for md_node in md_nodes:
    print(md_node)
    k += 1
    if k == 7:
        break
'''