from io import BytesIO

from markitdown import MarkItDown

from ..core.enums import Language


def convert2md(data: bytes) -> str:
    markitdown = MarkItDown()
    result = markitdown.convert(BytesIO(data))
    return result.text_content


def convert_language2text(file: bytes, language: Language) -> str:
    content = file.decode("utf-8")
    return content
