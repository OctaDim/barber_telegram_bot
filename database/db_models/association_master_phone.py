from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class MasterPhoneAssociation(Base):
    __tablename__ = "master_phone_association"

    master_id: Mapped[int] = mapped_column(ForeignKey("master.id"),
                                           primary_key=True)

    phone_id: Mapped[int] = mapped_column(ForeignKey("phone.id"),
                                          primary_key=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)