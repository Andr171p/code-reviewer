from collections.abc import Iterator

import logging
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_core.language_models import BaseChatModel
from pydantic import BaseModel, Field

from .utils import create_llm_chain_with_structured_output
from .prompts import DESCRIPTION_GENERATOR_PROMPT

logger = logging.getLogger(__name__)

FILE_EXTENSIONS: list[str] = [".bsl"]


class ModuleDescription(BaseModel):
    type: str = Field(description="Тип модуля")
    purpose: str = Field(description="Основное назначение модуля")
    details: str = Field(description="Дополнительные детали")


class BSLContextEnrichmentDirectoryLoader(BaseLoader):
    def __init__(
            self,
            dir_path: str | Path,
            *,
            encoding: str = "utf-8",
            file_extensions: list[str] | None = None,
            exclude_dirs: list[str] | None = None,
            llm: BaseChatModel | None = None
    ) -> None:
        """Загружает и обогащает контекст .bsl модулей из 1С проекта

        :param dir_path: Путь до директории с проектом.
        :param encoding: Кодировка при чтении.
        :param file_extensions: Разрешённые расширения файлов.
        :param exclude_dirs: Директории которые нужно исключить.
        :param llm: LLM для обогащения контекста.
        """
        self.dir_path = Path(dir_path).resolve()
        self.encoding = encoding
        self.file_extensions = FILE_EXTENSIONS if not file_extensions else file_extensions
        self.exclude_dirs = exclude_dirs
        self.llm = llm

    def lazy_load(self) -> Iterator[Document]:
        for file_path in self._walk_directory():
            try:
                content = self._read_file(file_path)
                metadata: dict[str, str] = {
                    "project": self.dir_path.name,
                    "filename": file_path.name,
                    "path": file_path.relative_to(self.dir_path)
                }
                description = self._generate_description(content, metadata)
                metadata.update({
                    "type": description.type,
                    "purpose": description.purpose,
                    "details": description.details
                })
                yield Document(page_content=content, metadata=metadata)
            except Exception as e:
                logger.exception(
                    "Error occurred while process file: %s; Error: %s",
                    file_path, e
                )
                continue

    def _should_skip(self, dir_name: str) -> bool:
        """Проверяет нужно пропустить директорию.

        :param dir_name: Имя директории.
        :return: True если да, False если нет
        """
        if self.exclude_dirs and dir_name in self.exclude_dirs:
            return True
        return False

    def _is_target_file(self, file_path: Path) -> bool:
        """Проверка на загрузку файла.

        :param file_path: Путь до проверяемого файла.
        :return: True если да, False если нет.
        """
        if file_path.suffix.lower() in self.file_extensions and file_path.is_file():
            return True
        return False

    def _read_file(self, file_path: Path) -> str:
        try:
            with open(file_path, encoding=self.encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            return ""

    def _walk_directory(self) -> Iterator[Path]:
        for path in self.dir_path.glob("*"):
            if path.is_file() and self._is_target_file(path):
                if self.exclude_dirs:
                    skip = False
                    for parent in path.parents:
                        if self._should_skip(parent.name):
                            skip = True
                            break
                    if skip:
                        continue
            yield path

    def _generate_description(
            self, content: str, metadata: dict[str, str]
    ) -> ModuleDescription:
        llm_chain = create_llm_chain_with_structured_output(
            output_schema=ModuleDescription,
            prompt_template=DESCRIPTION_GENERATOR_PROMPT,
            llm=self.llm
        )
        description = llm_chain.invoke({
            "project": metadata.get("project", ""),
            "filename": metadata.get("filename", ""),
            "file_path": metadata.get("file_path", ""),
            "content": content
        })
        return description
