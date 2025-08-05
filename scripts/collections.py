import logging

import weaviate
from weaviate.classes.config import Configure, Property, DataType
from weaviate.exceptions import SchemaValidationError, UnexpectedStatusCodeError

from src.code_reviewer.settings import settings

logger = logging.getLogger(__name__)

client = weaviate.connect_to_custom(
    http_host=settings.weaviate.http_host,
    http_port=settings.weaviate.http_port,
    http_secure=False,
    grpc_host=settings.weaviate.grpc_host,
    grpc_port=settings.weaviate.grpc_port,
    grpc_secure=False,
)

client.is_ready()


def create_dev_collection() -> None:
    try:
        client.collections.create(
            name="DevCollection",
            description="Коллекция для хранения материалов для разработки на 1С",
            vector_config=[
                Configure.Vectors.self_provided(
                    name="content",
                    vector_index_config=Configure.VectorIndex.hnsw()
                )
            ],
            properties=[
                Property(
                    name="content",
                    description="Часть кода",
                    data_type=DataType.TEXT
                )
            ]
        )
    except (SchemaValidationError, UnexpectedStatusCodeError):
        logger.exception("Error creating code collection: {e}")


def main() -> None:
    create_dev_collection()
    client.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
