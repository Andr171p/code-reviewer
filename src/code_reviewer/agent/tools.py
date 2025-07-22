import logging

from langchain_core.tools import BaseTool, ArgsSchema

logger = logging.getLogger(__name__)


class MemoryTool(BaseTool):
    name: str = "memory_tool"
    description: str = ""
    args_schema: ArgsSchema | None = ...

    def _run(self, ) -> ...:
        ...

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
