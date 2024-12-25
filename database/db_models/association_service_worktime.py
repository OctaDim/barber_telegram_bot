from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base

class ServiceWorkTimeAssociation(Base):
    __tablename__ = "service_worktime_association"

    # ### many repeated service_id - work_time_id pairs can be saved ###
    id: Mapped[int] = mapped_column(primary_key=True)

    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    work_time_id: Mapped[int] = mapped_column(ForeignKey("work_time.id"))

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)

# ##### For only one unique service_id - work_time_id pair saving ######
# class ServiceWorkTimeAssociation(Base):
#     __tablename__ = "service_worktime_association"
#     service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), primary_key=True)
#     work_time_id: Mapped[int] = mapped_column(ForeignKey("work_time.id"), primary_key=True)
# ######################################################################
