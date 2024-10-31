from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.db_connection import Base
from database.db_models.category_model import Category
from database.db_models.user_model import User


class Master(Base):
    __tablename__ = "master"

    id: Mapped[int] = mapped_column(primary_key=True)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("category.id"),
        nullable=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"),
        nullable=False,
        unique=True)

    full_name: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[str]

    qualification: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    note: Mapped[Optional[str]]

    image: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(),
                                              nullable=True)


# Master - Category - Master
# orm relations one-to-many
Master.master_categories = relationship(
    argument=Category,
    order_by=Category.name,
    # single_parent=True,  # One-to-one relations
    back_populates="category_masters")

Category.category_masters = relationship(
    argument=Master,
    order_by=Master.full_name,
    back_populates="master_categories")

# Master - User - Master
# orm relations one-to-one
Master.as_user = relationship(
    argument=User,
    order_by=User.full_name,
    single_parent=True,  # One-to-one relations
    back_populates="as_master")

User.as_master = relationship(
    argument=Master,
    order_by=Master.full_name,
    single_parent=True,  # One-to-one relations
    back_populates="as_user")
