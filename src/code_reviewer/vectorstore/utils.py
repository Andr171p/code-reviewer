from typing import Any

from uuid import UUID

from weaviate import WeaviateAsyncClient

from .schemas import modules_schema


def create_schema(project_id: UUID) -> dict[str, Any]:
    modules_schema["class"] = f"ModulesProject{project_id}"
    return modules_schema
