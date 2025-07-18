from .separators import *  # noqa: F403

from ..core.enums import ProgramingLanguage

LANGUAGE2SEPARATORS: dict[ProgramingLanguage: list[str]] = {
    ProgramingLanguage.ONEC: ONEC_SEPARATORS,  # noqa: F405
    ProgramingLanguage.C: CPP_SEPARATORS,  # noqa: F405
    ProgramingLanguage.CPP: CPP_SEPARATORS  # noqa: F405
}

ENRICHED_CHUNK_TEMPLATE = """Файл: {filename}
Код: {content}
Описание: {description}
Язык программирования: {language}
"""
