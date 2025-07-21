from ..core.enums import Language
from .separators import BSL_SEPARATORS

MIN_CHUNK_LENGTH = 15

LANGUAGE2SEPARATORS: dict[Language: list[str]] = {
    Language.ONEC: BSL_SEPARATORS
}
