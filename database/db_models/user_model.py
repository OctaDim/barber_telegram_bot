from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.association_user_role import UserRoleAssociation
from database.db_models.association_user_status import UserStatusAssociation


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    username: Mapped[str] = mapped_column(unique=True)

    full_name: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]

    phone_number: Mapped[Optional[str]]
    birth_date: Mapped[Optional[datetime]]
    description: Mapped[Optional[str]]

    blocked: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    user_statuses: Mapped[list['UserStatus']] = relationship(
        argument='UserStatus',
        secondary='user_status_association',
        order_by='UserStatus.name',
        back_populates='status_users'
    )

    user_roles: Mapped[list['UserRole']] = relationship(
        argument='UserRole',
        secondary='user_role_association',
        order_by='UserRole.name',
        back_populates='role_users'
    )

    client_work_times: Mapped[list['WorkTime']] = relationship(
        argument='WorkTime',
        secondary='work_time_user_association',
        order_by='WorkTime.time_start',
        back_populates="work_time_clients")

    user_masters: Mapped['Master'] = relationship(
        argument='Master',
        order_by='Master.full_name',
        back_populates="master_user")

    @property
    def user_contact(self) -> Optional[str]:
        if self.full_name and self.phone_number:
            return f"{self.full_name}, {self.phone_number}"
        if self.full_name:
            return f"{self.full_name}, {self.username}"
        if self.phone_number:
            return f"{self.phone_number}, {self.username}"
        return str(self.username)
