from typing import Callable

from collections.abc import Iterator

from langchain_core.documents import Document
from langchain_community.document_loaders import GithubFileLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from .base import BasePreprocessor
from .splitters import BSLCodeSplitter

DEFAULT_BRANCH = "master"


def filter_file(file_path: str) -> bool:
    return not file_path.endswith(".xml")


class GitHubRepoPreprocessor(BasePreprocessor):
    def __init__(self, access_token: str, github_api_url: str) -> None:
        self.access_token = access_token
        self.github_api_url = github_api_url

    async def preprocess(
            self,
            repo: str,
            branch: str = DEFAULT_BRANCH,
            file_filter: Callable[[str], bool] = filter_file
    ) -> list[Document]:
        loader = GithubFileLoader(
            repo=repo,
            branch=branch,
            access_token=self.access_token,
            github_api_url=self.github_api_url,
            file_filter=file_filter,
        )
        documents = await loader.aload()
        processed_chunks: list[Document] = []
        for chunks in self._split_documents(documents):
            processed_chunks.extend(chunks)
        return processed_chunks

    @staticmethod
    def _split_documents(documents: list[Document]) -> Iterator[list[Document]]:
        for document in documents:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=600,
                chunk_overlap=20,
                length_function=len
            )
            file_path = document.metadata["path"]
            if file_path.endswith(".bsl"):
                splitter = BSLCodeSplitter()
            chunks = splitter.split_documents([document])
            yield chunks
