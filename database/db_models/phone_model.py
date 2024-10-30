from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils.types.phone_number import PhoneNumberType

from database.db_connection import Base
from telegram.config.configs import LANGUAGE_CONFIGS


class Phone(Base):
    __tablename__ = 'phone'

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(
        PhoneNumberType(region=LANGUAGE_CONFIGS.PHONE_NUMBER_REGION),
        unique=True)

    active: Mapped[bool] = mapped_column(default=True)

    creator_id: Mapped[Optional[int]]
    editor_id: Mapped[Optional[int]]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(onupdate=datetime.now(), nullable=True)
