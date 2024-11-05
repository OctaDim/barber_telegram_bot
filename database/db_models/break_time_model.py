from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database.db_connection import Base


class BreakTime(Base):
    __tablename__ = 'break_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    start_break: Mapped[datetime]
    end_break: Mapped[datetime]

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)

    break_time_masters: Mapped[list['Master']] = relationship(
        argument='Master',
        secondary='master_break_time_association',
        order_by='Master.full_name',
        back_populates='master_break_times')
