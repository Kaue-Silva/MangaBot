from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String


class Base(DeclarativeBase):
    pass


class MangaData(Base):
    __tablename__ = "mangas"

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    last_chapter = Column(Integer, unique=True)
    link = Column(String(200))

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, manga={self.name!r}, last_chapter={self.last_chapter!r}, link={self.link!r})"


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    chat_id = Column(Integer, unique=True)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, chat_id={self.chat_id!r})"
