import logging

from langchain_community.document_loaders import GithubFileLoader
from langchain_gigachat import GigaChat

from src.code_reviewer.splitters.bsl_code_splitter import BSLDocumentContextEnricher

logging.basicConfig(level=logging.INFO)

ACCESS_TOKEN = ""


loader = GithubFileLoader(
    repo="1C-Company/dt-demo-configuration",  # the repo name
    branch="master",  # the branch name
    access_token=ACCESS_TOKEN,
    github_api_url="https://api.github.com",
    file_filter=lambda file_path: file_path.endswith(
        ".bsl"
    ),  # load all markdowns files.
)

llm = GigaChat(
    credentials="",
    scope="",
    model="",
    verify_ssl_certs=False,
    profanity_check=False
)

documents = loader.load()

print(len(documents))

documents = documents[:5]

enricher = BSLDocumentContextEnricher(llm=llm)

enriched_documents = enricher.enrich_documents(documents)

for enriched_document in enriched_documents:
    print(enriched_document)
