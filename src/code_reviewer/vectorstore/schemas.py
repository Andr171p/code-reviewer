from typing import TypedDict

from weaviate.classes.config import Property


class CollectionSchema(TypedDict):
    name: str
    description: str
    properties: list[Property]
