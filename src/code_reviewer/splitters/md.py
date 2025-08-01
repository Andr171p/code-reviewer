from ..base import BaseTextSplitter, BaseChunk


class MDChunk(BaseChunk):
    ...

    def to_text(self) -> str:
        return f"""
        """


class MarkdownTextSplitter(BaseTextSplitter[MDChunk]):
    ...

    def split_text(self, text: str) -> list[MDChunk]:
        ...
