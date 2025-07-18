from typing import Optional, Literal

from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: UUID
    username: str
    role: ...
    created_at: datetime
    
    
class Developer(BaseModel):
    id: UUID
    user_id: UUID
    role: ...


class Project(BaseModel):
    id: UUID
    name: str
    description: str
    repository_url: Optional[str] = None
    users: list[UUID]
    created_at: datetime
    
    
class Task(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    type: str
    business_value: Literal["HIGHT", "MEDIUM", "LOW"]
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    
    
class CodeArtifact(BaseModel):
    id: UUID
    project_id: UUID
    name: str
    path: str
    content: str
    
    
class Finding(BaseModel):
    type: str
    message: str
    severity: Literal["CRITICAL", "HIGHT", "MEDIUM", "LOW"]
    code_snippet: str
    
    
class CodeReview(BaseModel):
    id: UUID
    name: str
    status: Literal["PENDING", "COMPLETED"]
    findings: list[Finding]
    artifacts: list[UUID]
