from datetime import datetime

from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class BreakTime(Base):
    __tablename__ = 'break_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    start_break: Mapped[datetime]
    end_break: Mapped[datetime]
    master_id: Mapped[int] = mapped_column(nullable=True)
