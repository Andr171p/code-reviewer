import pymupdf4llm

from langchain_text_splitters import RecursiveCharacterTextSplitter

from llama_index.core import Document
from llama_index.readers.file import PyMuPDFReader
from llama_index.core.node_parser import LangchainNodeParser

pdf_path = r"C:\Users\andre\CodeReviewer\Руководство-пользователя-83.004.04.pdf"

# md_text = pymupdf4llm.to_markdown(pdf_path)

reader = PyMuPDFReader()
docs = reader.load(pdf_path)

recursive_node_parser = LangchainNodeParser(RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=20,
    length_function=len,
))

nodes = recursive_node_parser.get_nodes_from_documents(docs)

