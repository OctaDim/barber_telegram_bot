
from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.association_user_role import UserRoleAssociation
from database.db_models.association_user_status import UserStatusAssociation
from database.db_models.user_role_model import UserRole
from database.db_models.user_status_model import UserStatus


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)

    status_id: Mapped[int] = mapped_column(
        ForeignKey("user_status.id"),
        nullable=True)

    role_id: Mapped[int] = mapped_column(
        ForeignKey("user_role.id"),
        nullable=False)

    telegram_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)

    full_name: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]
    phone_number: Mapped[Optional[str]]
    birth_date: Mapped[Optional[datetime]]
    description: Mapped[Optional[str]]

    blocked: Mapped[bool] = mapped_column(default=False)
    active: Mapped[bool] = mapped_column(default=True)

    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    @property
    def user_contact(self) -> Optional[str]:
        if self.full_name and self.phone_number:
            return f"{self.full_name}, {self.phone_number}"
        if self.full_name:
            return f"{self.full_name}, {self.username}"
        if self.phone_number:
            return "{self.phone_number}, {self.username}"
        return str(self.username)


# User - Status - User
# orm relations many-to-many
User.user_statuses = relationship(
    argument=UserStatus,
    secondary=UserStatusAssociation.__tablename__,
    order_by=UserStatus.name,
    back_populates="status_users")

UserStatus.status_users = relationship(
    argument=User,
    secondary=UserStatusAssociation.__tablename__,
    order_by=User.full_name,
    back_populates="user_statuses")

# User - Role - User
# orm relations many-to-many
User.user_roles = relationship(
    argument=UserRole,
    secondary=UserRoleAssociation.__tablename__,
    order_by=UserRole.name,
    back_populates="role_users")

UserRole.role_users = relationship(
    argument=User,
    secondary=UserRoleAssociation.__tablename__,
    order_by=User.full_name,
    back_populates="user_roles")
