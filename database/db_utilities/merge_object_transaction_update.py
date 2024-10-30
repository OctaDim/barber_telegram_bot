from sqlalchemy.orm import Session

from database.db_utilities.model_object_update import update_object_without_db_commit


def merge_obj_to_session_group_update(object_to_merge,
                                      new_update_data: dict,
                                      ongoing_session: Session) -> None:
    object_to_merge = update_object_without_db_commit(
        model_object=object_to_merge,
        new_update_data=new_update_data)

    ongoing_session.merge(object_to_merge)
