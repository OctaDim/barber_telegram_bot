from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped
)

from database.db_engine import url_engine
from database.db_connection import DBConnection

Base = declarative_base()



class Services(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()


if __name__ == '__main__':
    db_connector = DBConnection(db_url=url_engine)
    db_connector.create_tables(Base)
