from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base


class Master(Base):
    __tablename__ = "master"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        unique=True)

    full_name: Mapped[str]
    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]

    qualification: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    note: Mapped[Optional[str]]

    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    master_work_times: Mapped['WorkTime'] = relationship(
        argument='WorkTime',
        order_by='WorkTime.time_start',
        back_populates="work_time_masters")

    master_services: Mapped[list['Service']] = relationship(
        argument='Service',
        secondary='service_master_association',
        order_by='Service.name',
        back_populates="service_masters")

    master_categories: Mapped['Category'] = relationship(
        argument='Category',
        uselist=False,
        order_by='Category.name',
        back_populates="category_masters")

    master_user: Mapped['User'] = relationship(
        argument='User',
        uselist=False,
        order_by='User.full_name',
        back_populates="user_masters")

    master_phones: Mapped[list['Phone']] = relationship(
        argument='Phone',
        secondary='master_phone_association',
        order_by='Phone.number',
        back_populates="phone_masters")

    master_break_times: Mapped[list['BreakTime']] = relationship(
        'BreakTime',
        secondary='master_break_time_association',
        order_by='BreakTime.start_break',
        back_populates='break_time_masters')

    master_socials: Mapped[list['Social']] = relationship(
        argument='Social',
        uselist=False,
        order_by='Social.name',
        back_populates="social_masters")

    master_address: Mapped[list['Address']] = relationship(
        argument='Address',
        uselist=False,
        order_by='Address.street',
        back_populates="address_masters")

