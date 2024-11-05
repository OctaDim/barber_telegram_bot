from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=True)

    name: Mapped[str]
    price: Mapped[float]
    time_duration: Mapped[timedelta]
    description: Mapped[Optional[str]]

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    service_work_times: Mapped[list['WorkTime']] = relationship(
        argument='WorkTime',
        secondary='service_worktime_association',
        order_by='WorkTime.time_start',
        back_populates="work_time_services")

    service_categories: Mapped['Category'] = relationship(
        argument='Category',
        uselist=False,
        order_by='Category.name',
        back_populates="category_services")

    service_masters: Mapped[list['Master']] = relationship(
        argument='Master',
        secondary='service_master_association',
        order_by='Master.full_name',
        back_populates="master_services")