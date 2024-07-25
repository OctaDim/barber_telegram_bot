from datetime import datetime, timedelta

from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class WorkTime(Base):
    __tablename__ = 'work_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    start_time: Mapped[datetime]
    end_time: Mapped[datetime]
    delta: Mapped[timedelta]
    active: Mapped[bool] = mapped_column(default=False)
    reserved: Mapped[bool] = mapped_column(default=False)
    master_id: Mapped[int] = mapped_column(nullable=True)
