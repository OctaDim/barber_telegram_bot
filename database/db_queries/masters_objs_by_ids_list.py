from typing import List, Type

from sqlalchemy.orm import Session

from database.db_models.master_model import Master


def get_unique_masters_objs_by_ids_list(masters_ids_list: List[int],
                                        ongoing_session: Session
                                        ) -> List[Type[Master]]:
    masters_objs_list = ongoing_session.query(Master).filter(
        Master.id.in_(masters_ids_list)).all()

    return masters_objs_list
