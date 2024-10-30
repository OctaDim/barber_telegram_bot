from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class UserRoleAssociation(Base):
    __tablename__ = "user_role_association"

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),
                                         primary_key=True)

    role_id: Mapped[int] = mapped_column(ForeignKey("user_role.id"),
                                         primary_key=True)

    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)
