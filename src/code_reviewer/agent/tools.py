import logging

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, ArgsSchema, ToolException

from ..memory import RedisMemoryStorage, MemoryType

logger = logging.getLogger(__name__)


class StoreMemoryTool(BaseTool):
    name: str = "store_memory_tool"
    description: str = ""
    args_schema: ArgsSchema | None = ...

    def __init__(self, memory_storage: RedisMemoryStorage, **kwargs) -> None:
        super().__init__(**kwargs)
        self._memory_storage = memory_storage

    def _run(
            self,
            content: str,
            memory_type: MemoryType,
            metadata: dict[str, str] | None = None,
            config: RunnableConfig | None = None,
    ) -> str:
        config = config or RunnableConfig()
        user_id = config.get("user_id", "")
        thread_id = config.get("thread_id")
        try:
            ...
        except Exception as e:
            raise ToolException(...)

    async def _arun(self, ) -> ...:
        ...


class CodeGenerationTool(BaseTool):
    name: str = "code_agent"
    description: str = ""
    args_schema: ArgsSchema | None = ...

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        ...

    def _run(self, query: str) -> str:
        logger.info("---GENERATE CODE---")
        ...

    async def _arun(self, query: str) -> str:
        logger.info("---GENERATE CODE---")
        ...
