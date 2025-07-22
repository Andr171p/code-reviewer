from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class ProjectOrm(Base):
    __tablename__ = "projects"

    name: Mapped[str]
    version: Mapped[str | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, version={self.version})"

    def __repr__(self) -> str:
        return str(self)
