from langchain_core.documents import Document

from src.code_reviewer.splitters import BSLCodeSplitter

splitter = BSLCodeSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    enrich_chunks=False
)

with open("Module.bsl", encoding="utf-8") as file:
    content = file.read()


docs = splitter.split_documents([Document(page_content=content)])

for doc in docs:
    print("=" * 75)
    print(doc)
