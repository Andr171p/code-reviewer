import weaviate
from weaviate.classes.config import Property, DataType


client = weaviate.connect_to_custom(
    http_host="",
    http_port=...,
    http_secure=False,
    grpc_host="",
    grpc_port=...,
    grpc_secure=False
)

client.is_ready()

'''
try:
    documentations = client.schemas.create(
        name="Documentations",
        description="Документация для работы с 1С (статьи, руководства, книги)",
        properties=[
            Property(
                name="source",
                description="Имя источника",
                data_type=DataType.TEXT
            ),
            Property(
                name="content",
                description="Содержание чанка",
                data_type=DataType.TEXT
            ),
            Property(
                name="page",
                description="Страница к котрой относиться чанк",
                data_type=DataType.INT,
                skip_vectorization=True
            ),
            Property(
                name="total_pages",
                description="Общее количество страниц в источнике",
                data_type=DataType.INT,
                skip_vectorization=True
            )
        ],
    )
except Exception as e:
    print(e)

# client.schemas.delete("Documentations")
'''


try:
    modules = client.collections.create(
        name="Modules",
        description="Модули с .bsl 1С кодом",
        properties=[
            Property(
                name="project",
                description="Название проекта к которому относиться код",
                data_type=DataType.TEXT
            ),
            Property(
                name="filename",
                description="Название файла",
                data_type=DataType.TEXT
            ),
            Property(
                name="file_path",
                description="Путь до файла в проекте",
                data_type=DataType.TEXT
            ),
            Property(
                name="content",
                description="Исходный код модуля",
                data_type=DataType.TEXT
            ),
            Property(
                name="type",
                description="Тип модуля",
                data_type=DataType.TEXT
            ),
            Property(
                name="purpose",
                description="Основное назначение модуля",
                data_type=DataType.TEXT
            ),
            Property(
                name="details",
                description="Дополнительные детали",
                data_type=DataType.TEXT
            )
        ]
    )
except Exception as e:
    print(e)

# client.schemas.delete("Modules")

client.close()
