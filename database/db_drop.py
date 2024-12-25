from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_connection import Base

# ######################################################################
# ###### Very necessary imports to initialize Postgres DB tables #######
# ######################################################################
from database import db_initialization
# ######################################################################
# ######################################################################


db_connector = DBConnection(db_url=db_engine_url)
db_connector.drop_models(Base)
