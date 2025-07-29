from weaviate.classes.config import Property, DataType

MODULE_PROPERTIES: list[Property] = [
    Property(
        name="source",
        description="Источник от куда взят код",
        data_type=DataType.TEXT
    ),
    Property(
        name="project",
        description="Проект",
        data_type=DataType.TEXT
    ),
    Property(
        name="filename",
        description="Название файла с кодом",
        data_type=DataType.TEXT
    ),
    Property(
        name="path",
        description="Путь до файла с кодом внутри проекта",
        data_type=DataType.TEXT
    ),
    Property(
        name="content",
        description="Часть файла с кодом",
        data_type=DataType.TEXT
    ),
    Property(
        name="type",
        description="Тип модуля",
        data_type=DataType.TEXT
    ),
    Property(
        name="purpose",
        description="Цель модуля в проекте",
        data_type=DataType.TEXT
    ),
    Property(
        name="detail",
        description="Дополнительные детали",
        data_type=DataType.TEXT
    )
]

DOCS_PROPERTIES = [
    Property(
        name="source",
        description="Источник от куда взят материал",
        data_type=DataType.TEXT
    ),
    Property(
        name="content",
        description="Содержание",
        data_type=DataType.TEXT
    ),
    Property(
        name="page",
        description="Текущая страница",
        data_type=DataType.INT
    ),
    Property(
        name="total_page",
        description="Всего страниц",
        data_type=DataType.INT
    )
]
