import os
import logging
import xmltodict

from dotenv import load_dotenv
from aspose.cells import Workbook, SaveFormat
from langchain_gigachat import GigaChat

from src.code_reviewer.core.enums import Language
from src.code_reviewer.splitters.code_splitter import CodeSplitter
from xml_content import content

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

# docs = splitter.split_documents([Document(page_content=md_text)])

with open("Информация.xml", encoding="utf-8") as file:
    print(xmltodict.parse(file.read()))
