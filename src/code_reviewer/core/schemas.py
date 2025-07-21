from __future__ import annotations

from typing import Any

from uuid import UUID, uuid4
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from .enums import ModuleType, MetadataType
from ..utils.converters import convert2md


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    username: str
    role: ...
    created_at: datetime
    updated_at: datetime


class Project(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Unique ID in UUID format
    name: str                                # Name of project
    version: str                             # Version, recommend format: 1.0.0
    description: str                         # Description of project
    created_at: datetime | None = None       # Date of creation
    updated_at: datetime | None = None       # Date of update


class Documentation(BaseModel):
    project_id: UUID                         # Project ID for bind
    id: UUID = Field(default_factory=uuid4)  # Unique id in UUID format
    filename: str
    title: str                               # Title of documentation
    content: str                             # Documentation text in Markdown format
    created_at: datetime | None = None       # Date of creation documentation
    updated_at: datetime | None = None       # date of update documentation


class Module(BaseModel):
    project_id: UUID                         # Project ID for bind
    id: UUID = Field(default_factory=uuid4)  # Unique identifier of module
    type: ModuleType                         # Type of module
    metadata_link: UUID | None = None        # Link to metadata
    content: str                             # Source code of module


class Metadata(BaseModel):
    id: UUID                       # UUID of object
    type: MetadataType             # Type of object
    name: str                      # Object name
    synonym: str                   # Synonym of object
    comments: str | None = None    # Comments of metadata
    properties: dict[str, Any]     # Properties of object
    content: str                   # XML content of object
    child_objects: list[Metadata]  # Nested objects

    @field_validator("content", mode="before")
    def validate_content(cls, content: str) -> str:
        return convert2md(content.encode("utf-8"))
