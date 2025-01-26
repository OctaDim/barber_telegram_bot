from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)

    master_id: Mapped[int] = mapped_column(ForeignKey("master.id"))

    street: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)
    sort_index: Mapped[int] = mapped_column(nullable=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    address_masters: Mapped[list['Master']] = relationship(
        argument='Master',
        uselist=False,
        order_by='Master.full_name',
        back_populates="master_address")
