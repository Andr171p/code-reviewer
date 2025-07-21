import os
import logging

from dotenv import load_dotenv
from langchain_gigachat import GigaChat
from langchain_core.documents import Document

from src.code_reviewer.core.enums import Language
from src.code_reviewer.utils.converters import convert_language2text
from src.code_reviewer.splitters.code_splitter import CodeSplitter

logging.basicConfig(level=logging.INFO)

load_dotenv(".env")

llm = GigaChat(
    credentials=os.getenv("GIGACHAT_API_KEY"),
    scope=os.getenv("GIGACHAT_SCOPE"),
    model=os.getenv("GIGACHAT_MODEL"),
    profanity_check=False,
    verify_ssl_certs=False,
)

splitter = CodeSplitter(
    chunk_size=1000,
    chunk_overlap=20,
    length_function=len,
    language=Language.ONEC,
    enrich_chunks=True,
    llm=llm
)


with open("Module.bsl", "rb") as file:
    md_text = convert_language2text(file.read(), language=Language.ONEC)


docs = splitter.split_documents([Document(page_content=md_text)])

for doc in docs:
    print(doc)
