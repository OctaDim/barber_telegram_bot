from database.db_connection import DBConnection
from database.db_engine_url import db_engine_url
from database.db_models.master_model import Master


def get_user_telegram_id_by_master_id(
        master_id: int
):
    with DBConnection(db_url=db_engine_url) as session:
        master_obj = session.query(Master).filter(
            Master.id == master_id).first()

        return master_obj.master_user.telegram_id
