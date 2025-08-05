from typing import Any

from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from ulid import ULID

DEFAULT_MEMORY_METADATA = "{}"


class AgentMode(StrEnum):
    """Режимы работы ИИ агента.

    Attributes:
        DEFAULT: Стандартный режим (поддерживает QA, tools calling, mcp)
        RESEARCHER: Режим для задач требующих проведения исследования.
        REASONER: Для сложных задач требующих рассуждений и планирования.
    """
    DEFAULT = "default"
    REVIEWER = "reviewer"
    RESEARCHER = "researcher"
    REASONER = "reasoner"


class MemoryType(StrEnum):
    """Определяет тип долгосрочной памяти
    для категоризации и извлечения информации.

    Attributes:
        EPISODIC: Личный опыт и предпочтения пользователя.
        SEMANTIC: Общие знания предметной области и факты.
    """
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class Memory(BaseModel):
    """Модель долгосрочной памяти"""
    key: str | None = None
    id: ULID = Field(default_factory=ULID)
    user_id: str = Field(default="system")
    thread_id: str | None = None
    content: str = Field(description="Знания которые нужно сохранить")
    memory_type: MemoryType | None = None
    metadata: str = Field(
        default=DEFAULT_MEMORY_METADATA, description="Дополнительные метаданные"
    )
    created_at: datetime = Field(default_factory=datetime.now)


class Document(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
