from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class WorkTimeUserAssociation(Base):
    __tablename__ = "work_time_user_association"

    # ### many repeated service_id - work_time_id pairs can be saved ###
    id: Mapped[int] = mapped_column(primary_key=True)

    work_time_id: Mapped[int] = mapped_column(ForeignKey("work_time.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)
