import time
import enum
from typing import Annotated, Optional

from sqlalchemy import (
    TIMESTAMP,
    Column,
    Enum,
    ForeignKey,
    Integer,
    MetaData,
    PrimaryKeyConstraint,
    String,
    Table,
    CheckConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
str_32 = Annotated[str, 32]
str_128 = Annotated[str, 128]
str_256 = Annotated[str, 256]
intfg_user_id_del = Annotated[int, ForeignKey("users.id", ondelete="CASCADE")]
intfg_user_id = Annotated[int, ForeignKey("users.id")]

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}


class Base(DeclarativeBase):

    metadata = MetaData(naming_convention=naming_convention)

    type_annotation_map = {
        str_32: String(32),
        str_128: String(128),
        str_256: String(256)
    }

    repr_cols_num = 3
    repr_cols = tuple()
    
    def __repr__(self):
        """Relationships не используются в repr(), т.к. могут вести к неожиданным подгрузкам"""
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"

class Users(Base):
    """Модель пользователя"""

    __tablename__ = 'users'

    id: Mapped[intpk]
    vk_id: Mapped[int] = mapped_column(index=True, unique=True)
    first_name: Mapped[Optional[str_32]]
    last_name: Mapped[Optional[str_32]] 
    last_seen: Mapped[int] = mapped_column(default=round(time.time()))
    secret_word_hash: Mapped[str_256]

    def __repr__(self) -> str:
        return '{}'.format(self.id)

    def set_secret_word(self, word):
        self.secret_word_hash = generate_password_hash(word)

    def check_secret_word(self, word):
        return check_password_hash(self.secret_word_hash, word)

class Chats(Base):
    """Существующие беседы пользователя"""

    __tablename__ = 'chats'
    __table_args__ = (
        CheckConstraint("type in ('private', 'conversation')", name="ck_type_of_user_conversation"),
    )
    id: Mapped[intpk]
    peer_id: Mapped[int] = mapped_column(index=True, unique=True)
    type: Mapped[str] = mapped_column(default='private')
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    def __repr__(self) -> str:
        return '{}'.format(self.id)