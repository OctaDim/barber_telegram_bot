from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm.decl_api import DeclarativeMeta

from telegram.config.logging import LOGGING
from telegram.params.user_role_text import USER_ROLES_ENUM

Base = declarative_base()


class DBConnection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(url=db_url, echo=LOGGING.ORM_RAW_SQL_CONSOLE)
        self.Session = sessionmaker(bind=self.engine)

    def __enter__(self):
        self.session = self.Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def create_tables(self, base: DeclarativeMeta):
        base.metadata.create_all(self.engine, checkfirst=True)
        self._create_user_roles(base)

    def _create_user_roles(self, base: DeclarativeMeta):
        UserRole = base.registry._class_registry['UserRole']

        with self as session:
            roles = USER_ROLES_ENUM.roles

            for role_name in roles:
                session.add(UserRole(name=role_name))

            session.commit()
