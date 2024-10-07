from datetime import timedelta, datetime

from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database.db_models.services_model import Services


class WorkTime(Base):
    __tablename__ = 'work_time'

    id: Mapped[int] = mapped_column(primary_key=True)

    time_start: Mapped[datetime]
    time_end: Mapped[datetime]
    slot_duration: Mapped[timedelta]
    active: Mapped[bool] = mapped_column(default=False)
    reserved: Mapped[bool] = mapped_column(default=False)
    master_id: Mapped[int] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(nullable=True)
    service: Mapped[int] = mapped_column(ForeignKey('services.id'), nullable=True)


WorkTime.service_rel = relationship("Services", back_populates="work_times")
Services.work_times = relationship("WorkTime", order_by=WorkTime.id, back_populates="service_rel")
