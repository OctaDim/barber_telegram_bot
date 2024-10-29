def update_object(data: dict, obj, session):
    for key, values in data.items():
        if hasattr(obj, key):
            setattr(obj, key, values)

            session.commit()


def update_object_without_db_commit(model_object, new_update_data: dict):
    for attr_name, attr_value in new_update_data.items():
        setattr(model_object, attr_name, attr_value)
    return model_object
