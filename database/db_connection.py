from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta


# The common Base metamodel used to create models in a separate modules packages
Base = declarative_base()


class DBConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self.session.close()

    def create_tables(self, base: DeclarativeMeta):
        base.metadata.create_all(self.engine, checkfirst=True)
