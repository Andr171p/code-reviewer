from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, Field
from ulid import ULID


class MemoryType(StrEnum):
    """Определяет тип долгосрочной памяти
    для категоризации и извлечения информации.

    :param EPISODIC: Личный опыт и предпочтения пользователя.
    :param SEMANTIC: Общие знания предметной области и факты.
    """
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


class Memory(BaseModel):
    """Модель долгосрочной памяти"""
    content: str = Field(description="Знания которые нужно сохранить")
    memory_type: MemoryType = Field(description="Тип памяти")
    metadata: str = Field(description="Дополнительные метаданные")


class StoredMemory(Memory):
    """Сохранённая модель памяти"""
    key: str                                                    # Redis key
    id: ULID = Field(default_factory=ULID)                      # Уникальный идентификатор памяти
    user_id: str | None = None                                  # ID пользователя
    thread_id: str | None = None                                # ID потока
    memory_type: MemoryType | None = None                       # Тип памяти
    created_at: datetime = Field(default_factory=datetime.now)  # Дата создания
