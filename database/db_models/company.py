from sqlalchemy.orm import (
    declarative_base,
    mapped_column,
    Mapped,
)

from sqlalchemy_utils.types.phone_number import PhoneNumberType

from database.db_engine import url_engine
from database.db_connection import DBConnection

Base = declarative_base()


class Services(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()


class Phone(Base):
    __tablename__ = 'phone'

    id: Mapped[int] = mapped_column(primary_key=True)

    number: Mapped[str] = mapped_column(PhoneNumberType(region="BY"), unique=True)


class Socials(Base):
    __tablename__ = 'socials'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column(unique=True)



class Address(Base):
    __tablename__ = 'address'

    id: Mapped[int] = mapped_column(primary_key=True)

    street: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)


if __name__ == '__main__':
    db_connector = DBConnection(db_url=url_engine)
    db_connector.create_tables(Base)
