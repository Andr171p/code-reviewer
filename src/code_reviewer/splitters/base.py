from abc import ABC, abstractmethod


class BaseSplitter(ABC):
    def split_text(self, text: str) -> list[...]:
        ...
