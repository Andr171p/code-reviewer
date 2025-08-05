from ..schemas import AgentMode

ROUTING: dict[AgentMode, str] = {
    AgentMode.DEFAULT: "react",
    AgentMode.RESEARCHER: "researcher",
    AgentMode.REASONER: "reasoner"
}

FORMATED_MODULE_PROPERTIES = """**Проект**: %s
**Имя модуля**: %s
**Путь до модуля в проекте**: %s
**Код**: 
```bsl
%s
```
**Тип**: %s
**Цель в проекте**: %s
**Дополнительные детали**: %s
"""

FORMATED_DOCS_PROPERTIES = """
"""
