from redisvl.schema import IndexSchema

memory_schema = IndexSchema.from_yaml(
    r"/schemas/redis/memory.yaml"
)
