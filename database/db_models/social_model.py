from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class Social(Base):
    __tablename__ = 'social'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]
    url: Mapped[str] = mapped_column(nullable=True, unique=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)
