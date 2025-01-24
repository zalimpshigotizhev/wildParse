from datetime import datetime
from typing import Dict, Any

from sqlalchemy import Integer, TIMESTAMP, func
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, declared_attr

from const import asyncpg_url

engine = create_async_engine(url=asyncpg_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + 's'

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        """Строковое представление объекта для удобства отладки."""
        return f"<{self.__class__.__name__}(id={self.id}, created_at={self.created_at}, updated_at={self.updated_at})>"

