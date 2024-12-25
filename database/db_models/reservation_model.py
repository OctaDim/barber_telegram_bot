from datetime import datetime, timedelta
from typing import Optional, List

from sqlalchemy import ARRAY, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class Reservation(Base):
    __tablename__ = "reservation"

    id: Mapped[int] = mapped_column(primary_key=True)

    client_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"),
                                                nullable=False)
    reservation_date: Mapped[datetime]

    reserved_interval_first_slot_id: Mapped[int]
    reserved_slots_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))

    reserved_interval_time_start: Mapped[datetime]
    master_interval_time_end: Mapped[datetime]
    client_interval_time_end: Mapped[datetime]

    master_interval_duration: Mapped[timedelta]
    client_interval_duration: Mapped[timedelta]
    interval_time_loss: Mapped[timedelta]

    reserved_services_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    reserved_services_total_cost: Mapped[float]
    reserved_services_total_duration: Mapped[timedelta]

    archive_name_per_service: Mapped[dict] = mapped_column(JSON)
    archive_price_per_service: Mapped[dict] = mapped_column(JSON)
    archive_duration_per_service: Mapped[dict] = mapped_column(JSON)

    reserved_masters_ids: Mapped[List[int]] = mapped_column(ARRAY(Integer))
    archive_name_per_master: Mapped[dict] = mapped_column(JSON)

    cancelled_by_client: Mapped[bool] = mapped_column(default=False)
    cancelled_by_admin: Mapped[bool] = mapped_column(default=False)
    cancelled_by_admin_id: Mapped[Optional[int]]

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)
