from io import BytesIO
from urllib.parse import urlparse

from markitdown import MarkItDown


def convert2md(data: bytes) -> str:
    markitdown = MarkItDown()
    result = markitdown.convert(BytesIO(data))
    return result.text_content


def convert_language2text(file: bytes) -> str:
    content = file.decode("utf-8")
    return content


def get_github_repo_name(repo_url: str) -> str:
    repo_url = repo_url.replace("https://api.github.com", "")
    parts = repo_url.split("/")
    return f"{parts[1]}/{parts[2]}"


print(get_github_repo_name("https://api.github.com/1C-Company/dt-demo-configuration/blob/master/DemoConfDT/src/WebServices/MAExchange/Module.bsl"))
