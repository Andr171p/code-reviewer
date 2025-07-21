
modules_schema = {
    "class": "Modules",
    "description": "A collection of .bsl modules",
    "vectorizer": "text2vec-huggingface",
    "moduleConfig": {
        "text2vec-huggingface": {
            "model": f"{...}"
        }
    },
    "properties": [
        {
            "name": "project_id",
            "description": "Unique identifier of project",
            "dataType": ["uuid"],
            "moduleConfig": {"text2vec-huggingface": {"skip": True}}
        },
        {
            "name": "project",
            "description": "Name of 1C project",
            "dataType": ["string"]
        },
        {
            "name": "type",
            "description": "Type of module",
            "dataType": ["string"]
        },
        {
            "name": "content",
            "description": "Source code",
            "dataType": ["text"]
        },
        {
            "name": "description",
            "description": "Source code description",
            "dataType": ["text"]
        },
        {
            "name": "tags",
            "description": "Tags for improve search",
            "dataType": ["string"]
        }
    ]
}
