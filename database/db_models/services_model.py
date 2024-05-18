from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import timedelta


class Services(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    time_duration: Mapped[timedelta]
