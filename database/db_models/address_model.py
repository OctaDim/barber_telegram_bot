from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)

    street: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)
