from typing import Optional

from pydantic import BaseModel, field_validator


class BaseEnrichmentTextChunk(BaseModel):
    title: str
    h1: Optional[str] = None
    h2: Optional[str] = None
    h3: Optional[str] = None
    content: str
    summary: str
    keywords: list[str]
    page: Optional[int] = None
    
    @field_validator("keywords", mode="after")
    def validate_keywords(cls, keywords: list[str]) -> str:
        return " ".join(keywords)
    
    def to_text(self) -> str:
        raise NotImplementedError
    
    
class EnrichmentTextChunk(BaseEnrichmentTextChunk):
    def to_text(self) -> str:
        return f"""Название: {self.title}
        Содержание: {self.content}
        Краткое содержание: {self.summary}
        Ключевые слова: {self.keywords}
        Страница: {self.page}
        """
        

class EnrichmentWithHeadersTextChunk(BaseEnrichmentTextChunk):
    def to_text(self) -> str:
        return f"""Название: {self.title}
        Главный заголовок: {self.h1}
        Подзаголовок: {self.h2}
        Мелкий заголовок: {self.h3}
        Содержание: {self.content}
        Краткое содержание: {self.summary}
        Ключевые слова: {self.keywords}
        """
