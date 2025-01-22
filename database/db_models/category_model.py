from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True)

    master_id: Mapped[int] = mapped_column(
        ForeignKey("master.id"),
        nullable=True)

    name: Mapped[str] = mapped_column()
    description: Mapped[Optional[str]]

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    category_services: Mapped['Service'] = relationship(
        argument='Service',
        order_by='Service.name',
        back_populates="service_categories")

    category_masters: Mapped['Master'] = relationship(
        argument='Master',
        order_by='Master.full_name',
        back_populates="master_categories")
