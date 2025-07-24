from io import BytesIO

from markitdown import MarkItDown


def convert2md(data: bytes) -> str:
    markitdown = MarkItDown()
    result = markitdown.convert(BytesIO(data))
    return result.text_content


def convert_language2text(file: bytes) -> str:
    content = file.decode("utf-8")
    return content
