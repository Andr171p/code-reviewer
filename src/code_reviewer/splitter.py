from typing import AnyStr

import re

BSL_PATTERNS: dict[str, re.Pattern[AnyStr]] = {
    "procedure": re.compile(
        r"^\s*(?:Процедура|Procedure)\s+([\wа-яА-Я]+)\s*(?:\(([^)]*)\))?\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "function": re.compile(
        r"^\s*(?:Функция|Function)\s+([\wа-яА-Я]+)\s*(?:\(([^)]*)\))?\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_procedure": re.compile(
        r"^\s*(?:КонецПроцедуры|EndProcedure)\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_function": re.compile(
        r"^\s*(?:КонецФункции|EndFunction)\s*(?:\/\/.*)?$",
        re.IGNORECASE | re.MULTILINE
    ),
    "region": re.compile(
        r"^\s*#Область\s+(.*?)\s*$",
        re.IGNORECASE | re.MULTILINE
    ),
    "end_region": re.compile(
        r"^\s*#КонецОбласти\s*$",
        re.IGNORECASE | re.MULTILINE
    )
}



def split_code(code: str) -> list[dict[str, str | dict]]:
    chunks = []
    lines = code.split("\n")
    current_chunk = []
    chunk_type = None
    chunk_name = None
    chunk_meta = {}
    stack = []
    for i, line in enumerate(lines):
        # Проверяем начало новой конструкции
        if not chunk_type:
            for c_type, pattern in BSL_PATTERNS.items():
                match = pattern.match(line)
                if match:
                    if c_type in ["procedure", "function"]:
                        chunk_type = c_type
                        chunk_name = match.group(1)
                        chunk_meta = {
                            "params": match.group(2).split(",") if match.group(2) else [],
                            "start_line": i + 1
                        }
                        current_chunk.append(line)
                        break
                    elif c_type == "region":
                        stack.append(("region", match.group(1)))
                        current_chunk.append(line)
                        break
        else:
            current_chunk.append(line)

            # Проверяем конец текущей конструкции
            end_pattern = BSL_PATTERNS[f"end_{chunk_type}"]
            if end_pattern.match(line):
                chunks.append({
                    "type": chunk_type,
                    "name": chunk_name,
                    "content": "\n".join(current_chunk),
                    "meta": {
                        **chunk_meta,
                        "end_line": i + 1
                    }
                })
                current_chunk = []
                chunk_type = None
                chunk_name = None
                chunk_meta = {}

            # Для областей
            elif chunk_type == "region" and BSL_PATTERNS["end_region"].match(line):
                region_type, region_name = stack.pop()
                chunks.append({
                    "type": region_type,
                    "name": region_name,
                    "content": "\n".join(current_chunk),
                    "meta": {
                        "start_line": i - len(current_chunk) + 2,
                        "end_line": i + 1
                    }
                })
                current_chunk = []
                chunk_type = None

        # Добавляем оставшийся код как отдельный чанк
    if current_chunk:
        chunks.append({
            "type": "code",
            "name": "global_code",
            "content": "\n".join(current_chunk),
            "meta": {
                "start_line": max(1, len(lines) - len(current_chunk) + 1),
                "end_line": len(lines)
            }
        })

    return chunks


def get_chunk_info(chunk: dict) -> str:
    """Возвращает информацию о чанке в читаемом формате"""
    if chunk["type"] in ["procedure", "function"]:
        params = ", ".join(chunk["meta"]["params"])
        return f"{chunk["type"].title()} {chunk["name"]}({params})"
    elif chunk["type"] == "region":
        return f"Region: {chunk["name"]}"
    else:
        return "Global code"


def split_1c_code(code: str, min_chunk_size: int = 10) -> list[dict]:
    """
    Разбивает код 1С на логичные чанки (функции, процедуры, области)

    :param code: Исходный код на языке 1С
    :param min_chunk_size: Минимальный размер чанка (в строках)
    :return: Список чанков с метаданными
    """
    chunks = split_code(code)

    # Фильтрация слишком маленьких чанков
    return [chunk for chunk in chunks
            if len(chunk["content"].split("\n")) >= min_chunk_size
            or chunk["type"] in ["procedure", "function", "region"]]


# Пример кода на 1С
bsl_code = """
// Это пример модуля на 1С

#Область Инициализация

Процедура ПриИнициализации()
    // Код инициализации
    Перем ЛокальнаяПеременная;
КонецПроцедуры

#КонецОбласти

Функция РассчитатьСумму(Знач А, Знач Б)
    Если А > 0 И Б > 0 Тогда
        Возврат А + Б;
    Иначе
        Возврат 0;
    КонецЕсли;
КонецФункции

// Глобальный код
Сообщить("Привет, мир!");
"""

# Разбиваем код на чанки
chunks = split_1c_code(bsl_code)

# Выводим результат
for chunk in chunks:
    print(chunk)
    """print(f"\n--- {chunk["type"].upper()} "{chunk["name"]}" ---")
    print(f"Lines: {chunk["meta"]["start_line"]}-{chunk["meta"]["end_line"]}")
    print(chunk["content"][:100] + ("..." if len(chunk["content"]) > 100 else ""))"""