from typing import Annotated

from sqlalchemy import Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.database import Base


class Product(Base):
    name: Mapped[str]
    artikul: Mapped[Annotated[int, mapped_column(unique=True, index=True, nullable=False)]]
    price: Mapped[int]
    rating: Mapped[float]
    quantity: Mapped[int]
    auto_update: Mapped[bool] = mapped_column(Boolean, default=True)
