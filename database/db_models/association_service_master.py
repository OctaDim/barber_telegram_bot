from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.db_connection import Base


class ServiceMasterAssociation(Base):
    __tablename__ = "service_master_association"

    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"),
                                            primary_key=True)

    master_id: Mapped[int] = mapped_column(ForeignKey("master.id"),
                                           primary_key=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)
