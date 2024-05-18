from database.db_connection import Base
from sqlalchemy.orm import Mapped, mapped_column


class Socials(Base):
    __tablename__ = 'socials'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column(unique=True)
