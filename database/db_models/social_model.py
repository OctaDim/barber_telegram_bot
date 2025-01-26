from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base


class Social(Base):
    __tablename__ = 'social'

    id: Mapped[int] = mapped_column(primary_key=True)

    master_id: Mapped[int] = mapped_column(ForeignKey("master.id"))

    name: Mapped[str]
    social_username: Mapped[str] = mapped_column(nullable=True, unique=True)
    url: Mapped[str] = mapped_column(nullable=True, unique=True)
    sort_index: Mapped[int] = mapped_column(nullable=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    social_masters: Mapped[list['Master']] = relationship(
        argument='Master',
        uselist=False,
        order_by='Master.full_name',
        back_populates="master_socials")
