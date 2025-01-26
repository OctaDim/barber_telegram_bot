from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.association_user_status import UserStatusAssociation


class UserStatus(Base):
    __tablename__ = "user_status"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[Optional[str]]
    sort_index: Mapped[int] = mapped_column(nullable=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

    status_users: Mapped[list['User']] = relationship(
        argument='User',
        secondary=UserStatusAssociation.__tablename__,
        order_by='User.full_name',
        back_populates='user_statuses')
