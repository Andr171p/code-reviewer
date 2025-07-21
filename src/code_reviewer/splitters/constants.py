from .separators import BSL_SEPARATORS

from ..core.enums import Language

MIN_CHUNK_LENGTH = 15

LANGUAGE2SEPARATORS: dict[Language: list[str]] = {
    Language.ONEC: BSL_SEPARATORS
}
