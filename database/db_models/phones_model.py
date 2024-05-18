from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils.types.phone_number import PhoneNumberType


class Phone(Base):
    __tablename__ = 'phone'

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(PhoneNumberType(region="BY"), unique=True)
