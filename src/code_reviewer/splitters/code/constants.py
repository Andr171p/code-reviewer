from .separators import (
    ONEC_SEPARATORS,
    CPP_SEPARATORS,
)

from ...core.enums import ProgramingLanguage

LANGUAGE2SEPARATORS: dict[ProgramingLanguage: list[str]] = {
    ProgramingLanguage.ONEC: ONEC_SEPARATORS,
    ProgramingLanguage.C: CPP_SEPARATORS, 
    ProgramingLanguage.CPP: CPP_SEPARATORS
}

ENRICHED_CHUNK_TEMPLATE = """Файл: {filename}
Код: {content}
Описание: {description}
Язык программирования: {language}
"""
