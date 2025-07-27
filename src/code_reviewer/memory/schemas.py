from redisvl.schema import IndexSchema

memory_schema = IndexSchema.from_dict({
    "index": {
        "name": "long_term_memory",
        "prefix": "memory",
        "key_separator": ":",
        "storage_type": "json"
    },
    "fields": {
        {"name": "content", "type": "text"},
        {"name": "memery_type", "type": "tag"},
        {"name": "metadata", "type": "text"},
        {"name": "created_at", "type": "text"},
        {"name": "user_id", "type": "text"},
        {"name": "id", "type": "tag"},
        {
            "name": "embedding",
            "type": "vector",
            "attrs": {
                "algorithm": "flat",
                "dims": 2048,
                "distance_metric": "cosine",
                "datatype": "float32"
            }
        }
    }
})
