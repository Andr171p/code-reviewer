from pydantic import BaseModel


class EnrichmentChunk(BaseModel):
    filename: str
    content: str
    comments: str
    description: str
    keywords: list[str]
