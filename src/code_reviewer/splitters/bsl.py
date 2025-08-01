from typing import Any

from ..base import BaseTextSplitter, BaseChunk
from .constants import BSL_PATTERNS


class BSLChunk(BaseChunk):
    """Чанк с .bsl кодом"""
    type: str                 # Тип чанка
    name: str                 # Название логической части кода
    content: str              # Часть кода
    metadata: dict[str, Any]  # Метаданные (количество строк кода)

    def to_text(self) -> str:
        return f"""\
        **Type**: {self.type}
        **Name**: {self.name}
        **Code**: {self.content}
        **Lines**: {self.metadata["start_line"]}--{self.metadata["end_line"]}
        """


class BSLCodeSplitter(BaseTextSplitter[BSLChunk]):
    def split_text(self, text: str) -> list[BSLChunk]:
        chunks: list[BSLChunk] = []
        lines = text.split("\n")
        current_chunk: list[str] = []
        chunk_type: str | None = None
        chunk_name: str | None = None
        chunk_metadata: dict[str, Any] = {}
        stack = []
        for i, line in enumerate(lines):
            if not chunk_type:
                for type, pattern in BSL_PATTERNS.items():
                    match = pattern.match(line)
                    if match:
                        if type in ["procedure", "function"]:
                            chunk_type = type
                            chunk_name = match.group(1)
                            chunk_metadata = {
                                "params": match.group(2).split(",") if match.group(2) else [],
                                "start_line": i + 1
                            }
                            current_chunk.append(line)
                            break
                        elif type == "region":
                            stack.append(("region", match.group(1)))
                            current_chunk.append(line)
                            break
            else:
                current_chunk.append(line)
                end_pattern = BSL_PATTERNS[f"end_{chunk_type}"]
                if end_pattern.match(line):
                    chunks.append(BSLChunk(
                        type=chunk_type,
                        name=chunk_name,
                        content="\n".join(current_chunk),
                        metadata={**chunk_metadata, "end_line": i + 1}
                    ))
                    current_chunk = []
                    chunk_type = None
                    chunk_name = None
                    chunk_metadata = {}
                elif chunk_type == "region" and BSL_PATTERNS["end_region"].match(line):
                    region_type, region_name = stack.pop()
                    chunks.append(BSLChunk(
                        type=region_type,
                        name=region_name,
                        content="\n".join(current_chunk),
                        metadata={"start_line": i - len(current_chunk) + 2, "end_line": i + 1}
                    ))
                    current_chunk = []
                    chunk_type = None
        if current_chunk:
            chunks.append(BSLChunk(
                type="code",
                name="global_code",
                content="\n".join(current_chunk),
                metadata={
                    "start_line": max(1, len(lines) - len(current_chunk)),
                    "end_line": len(lines)
                }
            ))
        return chunks
