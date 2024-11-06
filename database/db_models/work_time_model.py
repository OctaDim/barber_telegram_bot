from datetime import timedelta, datetime
from typing import Optional, List

from sqlalchemy import ForeignKey, ARRAY, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from telegram.config.configs import LANGUAGE_CONFIGS
from sqlalchemy_utils.types.phone_number import PhoneNumberType

from database.db_connection import Base


class WorkTime(Base):
    __tablename__ = 'work_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    master_id: Mapped[int] = mapped_column(ForeignKey("master.id"))

    time_start: Mapped[datetime]
    time_end: Mapped[datetime]
    slot_duration: Mapped[timedelta]

    admin_name_client: Mapped[str] = mapped_column(nullable=True)
    admin_phone_client: Mapped[str] = mapped_column(
        PhoneNumberType(region=LANGUAGE_CONFIGS.PHONE_NUMBER_REGION),
        unique=True, nullable=True)

    selected_services: Mapped[List[int]] = mapped_column(ARRAY(Integer),
                                                         nullable=True)

    reserved: Mapped[bool] = mapped_column(default=False)
    admin_only: Mapped[bool] = mapped_column(default=False)

    is_group: Mapped[bool] = mapped_column(default=False)
    max_clients_limit: Mapped[int] = mapped_column(default=1)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    work_time_masters: Mapped['Master'] = relationship(
        'Master',
        uselist=False,
        order_by='Master.full_name',
        back_populates='master_work_times'
    )

    work_time_clients: Mapped[list['User']] = relationship(
        argument='User',
        secondary='work_time_user_association',
        order_by='User.full_name',
        back_populates="client_work_times")

    work_time_services: Mapped[list['Service']] = relationship(
        argument='Service',
        secondary='service_worktime_association',
        order_by='Service.name',
        back_populates="service_work_times")