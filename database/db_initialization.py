from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_connection import Base

# ######################################################################
# ###### Very necessary imports to initialize Postgres DB tables #######
# ######################################################################
from database.db_models.address_model import Address
from database.db_models.break_time_model import BreakTime
from database.db_models.category_model import Category
from database.db_models.master_model import Master
from database.db_models.phone_model import Phone
from database.db_models.service_model import Service
from database.db_models.social_model import Social
from database.db_models.user_model import User
from database.db_models.user_role_model import UserRole
from database.db_models.user_status_model import UserStatus
from database.db_models.work_time_model import WorkTime
from database.db_models.association_service_master import ServiceMasterAssociation
from database.db_models.association_service_worktime import ServiceWorkTimeAssociation
from database.db_models.association_user_role import UserRoleAssociation
from database.db_models.association_user_status import UserStatusAssociation

# ######################################################################
# ######################################################################


db_connector = DBConnection(db_url=db_engine_url)
db_connector.create_tables(Base)
