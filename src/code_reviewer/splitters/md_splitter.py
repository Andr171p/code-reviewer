from langchain_text_splitters import TextSplitter


class MarkdownSplitter(TextSplitter):
    def split_text(self, text: str) -> list[str]: ...
