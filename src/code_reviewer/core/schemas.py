from __future__ import annotations

from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    role: ...
    created_at: datetime
    updated_at: datetime
