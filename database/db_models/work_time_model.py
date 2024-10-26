from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.association_service_worktime import (
    ServiceWorkTimeAssociation)
from database.db_models.master_model import Master
from database.db_models.service_model import Service
from database.db_models.user_model import User


class WorkTime(Base):
    __tablename__ = 'work_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    master_id: Mapped[int] = mapped_column(
        ForeignKey("master.id"),
        nullable=True)

    client_user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=True)

    time_start: Mapped[datetime]
    time_end: Mapped[datetime]
    slot_duration: Mapped[timedelta]

    reserved: Mapped[bool] = mapped_column(default=False)
    admin_only: Mapped[bool] = mapped_column(default=False)

    active: Mapped[bool] = mapped_column(default=True)

    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)


# WorkTime - Master - WorkTime
# orm relations one-to-one
WorkTime.work_time_masters = relationship(
    argument=Master,
    order_by=Master.full_name,
    # single_parent=True,  # For one-to-one relations
    back_populates="master_work_times")

Master.master_work_times = relationship(
    argument=WorkTime,
    order_by=WorkTime.time_start,
    # single_parent=True,  # One-to-one relations
    back_populates="work_time_masters")

# WorkTime - Client_User - WorkTime
# orm relations one-to-many
WorkTime.work_time_clients = relationship(
    argument=User,
    order_by=User.full_name,
    back_populates="client_work_times")

User.client_work_times = relationship(
    argument=WorkTime,
    order_by=WorkTime.time_start,
    back_populates="work_time_clients")

# WorkTime - Srvice - WorkTime
# orm relations many-to-many
WorkTime.work_time_services = relationship(
    argument=Service,
    secondary=ServiceWorkTimeAssociation.__tablename__,
    order_by=Service.name,
    back_populates="service_work_times")

Service.service_work_times = relationship(
    argument=WorkTime,
    secondary=ServiceWorkTimeAssociation.__tablename__,
    order_by=WorkTime.time_start,
    back_populates="work_time_services")
