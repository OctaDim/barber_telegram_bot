from datetime import timedelta, datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.association_service_master import ServiceMasterAssociation
from database.db_models.category_model import Category
from database.db_models.master_model import Master


class Service(Base):
    __tablename__ = "service"

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=True)

    master_id: Mapped[int] = mapped_column(
        ForeignKey("master.id"),
        nullable=True)

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    price: Mapped[float]
    time_duration: Mapped[timedelta]
    description: Mapped[Optional[str]]

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)


# Service - Category - Service
# orm relations one-to-many
Service.service_categories = relationship(
    argument=Category,
    order_by=Category.name,
    back_populates="category_services")

Category.category_services = relationship(
    argument=Service,
    order_by=Service.name,
    back_populates="service_categories")

# Service - Master - Service
# orm relations many-to-many
Service.service_masters = relationship(
    argument=Master,
    secondary=ServiceMasterAssociation.__tablename__,
    order_by=Master.full_name,
    back_populates="master_services")

Master.master_services = relationship(
    argument=Service,
    secondary=ServiceMasterAssociation.__tablename__,
    order_by=Service.name,
    back_populates="service_masters")
