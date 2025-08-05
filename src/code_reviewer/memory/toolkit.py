from typing import cast

from langchain_core.tools import BaseTool, BaseToolkit
from pydantic import ConfigDict

from ..base import BaseMemoryStore
from .tools import BaseMemoryTool, RetrieveMemoriesTool, StoreMemoryTool


class LongTermMemoryManagementToolkit(BaseToolkit):
    """Toolkit для работы с долгосрочной памятью"""
    memory_store: BaseMemoryStore | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def get_tools(self) -> list[BaseTool]:
        tool_classes: list[type[BaseMemoryTool]] = [
            StoreMemoryTool, RetrieveMemoriesTool
        ]
        tools: list[BaseMemoryTool] = [
            tool_class.from_storage(storage=self.storage)
            for tool_class in tool_classes
        ]
        return cast(list[BaseTool], tools)
