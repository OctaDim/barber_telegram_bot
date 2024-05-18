from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_connection import Base

from database.db_models.address_model import Address
from database.db_models.phones_model import Phone
from database.db_models.socials_model import Socials
from database.db_models.services_model import Services

def models_used_in_process(address: Address,
                           phones: Phone,
                           socials: Socials,
                           services: Services,
                           ):
    """IMPORTANT: This function cannot be called anywhere. It is
    only used to show, that imports are necessary and that imported
    models are used when creating a new table with db_connector"""
    pass

db_connector = DBConnection(db_url=db_engine_url)
db_connector.create_tables(Base)
